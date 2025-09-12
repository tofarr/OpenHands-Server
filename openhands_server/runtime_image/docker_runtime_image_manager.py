
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import docker
from docker.errors import NotFound, APIError
from openhands_server.runtime_image.runtime_image_manager import RuntimeImageManager
from openhands_server.runtime_image.model import RuntimeImageInfo, RuntimeImageInfoPage, RuntimeImageStatus


@dataclass
class DockerRuntimeImageManager(RuntimeImageManager):

    client: docker.DockerClient = field(default_factory=docker.from_env)
    image_name: str = "ubuntu:latest"
    image_name_prefix: str = "ohrt-"

    def _image_name_from_id(self, runtime_image_id: UUID) -> str:
        """Generate image name from runtime image ID"""
        return f"{self.image_name_prefix}{runtime_image_id}"

    def _runtime_image_id_from_image_name(self, image_name: str) -> UUID | None:
        """Extract runtime image ID from image name"""
        if not image_name.startswith(self.image_name_prefix):
            return None
        try:
            return UUID(image_name[len(self.image_name_prefix):])
        except ValueError:
            return None

    def _image_to_runtime_image_info(self, image) -> RuntimeImageInfo | None:
        """Convert Docker image to RuntimeImageInfo"""
        # Try to get runtime image ID from image name/tag
        runtime_image_id = None
        for tag in image.tags:
            runtime_image_id = self._runtime_image_id_from_image_name(tag)
            if runtime_image_id:
                break
        
        if not runtime_image_id:
            # If no UUID found in tags, try to get from labels
            runtime_image_id_str = image.labels.get("runtime_image_id")
            if runtime_image_id_str:
                try:
                    runtime_image_id = UUID(runtime_image_id_str)
                except ValueError:
                    return None
            else:
                return None

        # Get metadata from labels with defaults
        image_name = image.labels.get("image_name", self.image_name)
        command = image.labels.get("command", "/bin/bash")
        working_dir = image.labels.get("working_dir", "/openhands/code")
        
        # Parse initial environment variables from labels
        initial_env = {}
        for key, value in image.labels.items():
            if key.startswith("env."):
                env_key = key[4:]  # Remove "env." prefix
                initial_env[env_key] = value

        # Get creation time
        created_at = datetime.fromisoformat(image.attrs["Created"].replace("Z", "+00:00"))

        # Get warm container counts from labels
        num_warm_containers = int(image.labels.get("num_warm_containers", "0"))
        target_num_warm_containers = int(image.labels.get("target_num_warm_containers", "0"))

        return RuntimeImageInfo(
            id=runtime_image_id,
            image_name=image_name,
            command=command,
            created_at=created_at,
            initial_env=initial_env,
            working_dir=working_dir,
            num_warm_containers=num_warm_containers,
            target_num_warm_containers=target_num_warm_containers
        )

    async def search_runtime_image_info(self, user_id: UUID | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeImageInfoPage:
        """Search for runtime images"""
        def _search():
            # Get all images with our prefix or label
            all_images = self.client.images.list()
            runtime_image_infos = []
            
            for image in all_images:
                # Check if this is one of our runtime images
                is_runtime_image = False
                
                # Check tags for our prefix
                for tag in image.tags:
                    if tag.startswith(self.image_name_prefix):
                        is_runtime_image = True
                        break
                
                # Check labels for runtime_image_id
                if not is_runtime_image and "runtime_image_id" in image.labels:
                    is_runtime_image = True
                
                if is_runtime_image:
                    runtime_image_info = self._image_to_runtime_image_info(image)
                    if runtime_image_info:
                        # Filter by user_id if specified (for future use)
                        # Currently not filtering by user_id as it's not in the model
                        runtime_image_infos.append(runtime_image_info)

            # Sort by creation time (newest first)
            runtime_image_infos.sort(key=lambda x: x.created_at, reverse=True)

            # Handle pagination
            start_idx = 0
            if page_id:
                try:
                    start_idx = int(page_id)
                except ValueError:
                    start_idx = 0

            end_idx = start_idx + limit
            page_items = runtime_image_infos[start_idx:end_idx]
            
            # Calculate next page ID
            next_page_id = str(end_idx) if end_idx < len(runtime_image_infos) else None

            return RuntimeImageInfoPage(items=page_items, next_page_id=next_page_id)

        return await asyncio.get_event_loop().run_in_executor(None, _search)

    async def get_runtime_image_info(self, id: UUID) -> RuntimeImageInfo | None:
        """Get a single runtime image info. Return None if the runtime image was not found."""
        def _get():
            # Try to find image by tag name first
            image_name = self._image_name_from_id(id)
            try:
                image = self.client.images.get(image_name)
                return self._image_to_runtime_image_info(image)
            except NotFound:
                pass
            
            # If not found by tag, search through all images for matching label
            try:
                all_images = self.client.images.list()
                for image in all_images:
                    if image.labels.get("runtime_image_id") == str(id):
                        return self._image_to_runtime_image_info(image)
                return None
            except APIError:
                return None

        return await asyncio.get_event_loop().run_in_executor(None, _get)

    async def batch_get_runtime_image_info(self, ids: list[UUID]) -> list[RuntimeImageInfo | None]:
        """Get a batch of runtime image info. Return None for any runtime image which was not found."""
        def _batch_get():
            results = []
            # Get all images once to avoid multiple API calls
            try:
                all_images = self.client.images.list()
                # Create lookup maps for efficiency
                tag_to_image = {}
                label_to_image = {}
                
                for image in all_images:
                    for tag in image.tags:
                        tag_to_image[tag] = image
                    runtime_image_id = image.labels.get("runtime_image_id")
                    if runtime_image_id:
                        label_to_image[runtime_image_id] = image
                
                # Look up each requested ID
                for runtime_image_id in ids:
                    image_name = self._image_name_from_id(runtime_image_id)
                    image = tag_to_image.get(image_name) or label_to_image.get(str(runtime_image_id))
                    
                    if image:
                        runtime_image_info = self._image_to_runtime_image_info(image)
                        results.append(runtime_image_info)
                    else:
                        results.append(None)
                        
            except APIError:
                # If there's an API error, return None for all requested IDs
                results = [None] * len(ids)
            
            return results

        return await asyncio.get_event_loop().run_in_executor(None, _batch_get)
