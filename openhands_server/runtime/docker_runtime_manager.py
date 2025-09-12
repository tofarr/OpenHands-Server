
import asyncio
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Optional

import docker
from docker.errors import NotFound, APIError
from pydantic import SecretStr

from openhands_server.runtime.runtime_manager import RuntimeManager
from openhands_server.runtime.runtime_info import RuntimeInfo
from openhands_server.runtime.runtime_status import RuntimeStatus
from openhands_server.runtime.page import RuntimeInfoPage


class DockerRuntimeManager(RuntimeManager):

    def __init__(
            self, 
            client: docker.DockerClient | None = None,
            runtime_name_prefix: str = "ohrt-",
            image_name: str = "ubuntu:latest",
        ):
        self.client = client or docker.DockerClient.from_env()
        self.runtime_name_prefix = runtime_name_prefix
        self.image_name = image_name

    def _container_name_from_id(self, runtime_id: UUID) -> str:
        """Generate container name from runtime ID"""
        return f"{self.runtime_name_prefix}{runtime_id}"

    def _runtime_id_from_container_name(self, container_name: str) -> UUID | None:
        """Extract runtime ID from container name"""
        if not container_name.startswith(self.runtime_name_prefix):
            return None
        try:
            return UUID(container_name[len(self.runtime_name_prefix):])
        except ValueError:
            return None

    def _docker_status_to_runtime_status(self, docker_status: str) -> RuntimeStatus:
        """Convert Docker container status to RuntimeStatus"""
        status_map = {
            "created": RuntimeStatus.STARTING,
            "restarting": RuntimeStatus.STARTING,
            "running": RuntimeStatus.RUNNING,
            "removing": RuntimeStatus.DELETED,
            "paused": RuntimeStatus.PAUSED,
            "exited": RuntimeStatus.PAUSED,
            "dead": RuntimeStatus.ERROR,
        }
        return status_map.get(docker_status.lower(), RuntimeStatus.ERROR)

    def _container_to_runtime_info(self, container) -> RuntimeInfo | None:
        """Convert Docker container to RuntimeInfo"""
        runtime_id = self._runtime_id_from_container_name(container.name)
        if not runtime_id:
            return None

        # Get user_id from labels
        user_id_str = container.labels.get("user_id")
        if not user_id_str:
            return None
        
        try:
            user_id = UUID(user_id_str)
        except ValueError:
            return None

        status = self._docker_status_to_runtime_status(container.status)
        
        # Generate URL and API key for running containers
        url = None
        session_api_key = None
        if status == RuntimeStatus.RUNNING:
            # In a real implementation, you'd get the actual exposed port and host
            # For now, using a placeholder
            url = f"http://localhost:8080"  # This should be dynamically determined
            session_api_key = SecretStr("placeholder-api-key")  # This should be generated/retrieved

        # Get creation time
        created_at = datetime.fromisoformat(container.attrs["Created"].replace("Z", "+00:00"))

        return RuntimeInfo(
            id=runtime_id,
            user_id=user_id,
            status=status,
            url=url,
            session_api_key=session_api_key,
            created_at=created_at
        )

    async def search_runtime_info(
        self, 
        user_id: UUID | None = None, 
        page_id: str | None = None, 
        limit: int = 100
    ) -> RuntimeInfoPage:
        """Search for runtimes"""
        def _search():
            # Build filters for Docker containers
            filters = {"name": f"{self.runtime_name_prefix}"}
            if user_id:
                filters["label"] = f"user_id={user_id}"

            containers = self.client.containers.list(all=True, filters=filters)
            runtime_infos = []
            
            for container in containers:
                runtime_info = self._container_to_runtime_info(container)
                if runtime_info:
                    runtime_infos.append(runtime_info)

            # Sort by creation time (newest first)
            runtime_infos.sort(key=lambda x: x.created_at, reverse=True)

            # Handle pagination
            start_idx = 0
            if page_id:
                try:
                    start_idx = int(page_id)
                except ValueError:
                    start_idx = 0

            end_idx = start_idx + limit
            page_items = runtime_infos[start_idx:end_idx]
            
            # Calculate next page ID
            next_page_id = str(end_idx) if end_idx < len(runtime_infos) else ""

            return RuntimeInfoPage(items=page_items, next_page_id=next_page_id)

        return await asyncio.get_event_loop().run_in_executor(None, _search)

    async def get_runtime_info(self, id: UUID) -> RuntimeInfo | None:
        """Get a single runtime info. Return None if the runtime was not found."""
        def _get():
            container_name = self._container_name_from_id(id)
            try:
                container = self.client.containers.get(container_name)
                return self._container_to_runtime_info(container)
            except NotFound:
                return None

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def batch_get_runtime_info(self, ids: list[UUID]) -> list[RuntimeInfo | None]:
        """Get a batch of runtime info. Return None for any runtime which was not found."""
        def _batch_get():
            results = []
            for runtime_id in ids:
                container_name = self._container_name_from_id(runtime_id)
                try:
                    container = self.client.containers.get(container_name)
                    runtime_info = self._container_to_runtime_info(container)
                    results.append(runtime_info)
                except NotFound:
                    results.append(None)
            return results

        return await asyncio.get_event_loop().run_in_executor(None, _batch_get)

    async def start_runtime(self, user_id: UUID) -> UUID:
        """Begin the process of starting a runtime. Return the UUID of the new runtime"""
        def _start():
            runtime_id = uuid4()
            container_name = self._container_name_from_id(runtime_id)
            
            # Create and start container with user_id label
            container = self.client.containers.run(
                self.image_name,
                name=container_name,
                labels={"user_id": str(user_id)},
                detach=True,
                # Add any additional configuration needed for the runtime
                # For example: ports, volumes, environment variables, etc.
            )
            
            return runtime_id

        return await asyncio.get_event_loop().run_in_executor(None, _start)

    async def resume_runtime(self, id: UUID) -> bool:
        """Begin the process of resuming a runtime. Return True if the runtime exists and is being resumed or is already running. Return False if the runtime did not exist"""
        def _resume():
            container_name = self._container_name_from_id(id)
            try:
                container = self.client.containers.get(container_name)
                if container.status == "paused":
                    container.unpause()
                elif container.status == "exited":
                    container.start()
                # If already running, that's fine too
                return True
            except NotFound:
                return False
            except APIError:
                return False

        return await asyncio.get_event_loop().run_in_executor(None, _resume)

    async def pause_runtime(self, id: UUID) -> bool:
        """Begin the process of pausing a runtime. Return True if the runtime exists and is being paused or is already paused. Return False if the runtime did not exist"""
        def _pause():
            container_name = self._container_name_from_id(id)
            try:
                container = self.client.containers.get(container_name)
                if container.status == "running":
                    container.pause()
                # If already paused or stopped, that's fine too
                return True
            except NotFound:
                return False
            except APIError:
                return False

        return await asyncio.get_event_loop().run_in_executor(None, _pause)

    async def delete_runtime(self, id: UUID) -> bool:
        """Begin the process of deleting a runtime (Which may involve stopping it first). Return False if the runtime did not exist"""
        def _delete():
            container_name = self._container_name_from_id(id)
            try:
                container = self.client.containers.get(container_name)
                # Stop the container if it's running
                if container.status in ["running", "paused"]:
                    container.stop()
                # Remove the container
                container.remove()
                return True
            except NotFound:
                return False
            except APIError:
                return False

        return await asyncio.get_event_loop().run_in_executor(None, _delete)

    async def __aenter__(self):
        """Start using this runtime manager"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Stop using this runtime manager"""
        if hasattr(self.client, 'close'):
            self.client.close()