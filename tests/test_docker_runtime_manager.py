import pytest
import asyncio
from uuid import uuid4
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from openhands_server.runtime.docker_runtime_manager import DockerRuntimeContainerManager
from openhands_server.runtime.runtime_status import RuntimeContainerStatus


class TestDockerRuntimeContainerManager:
    """Test cases for DockerRuntimeContainerManager"""

    def test_init(self):
        """Test DockerRuntimeContainerManager initialization"""
        manager = DockerRuntimeContainerManager(
            runtime_name_prefix="test-",
            image_name="test:latest"
        )
        assert manager.runtime_name_prefix == "test-"
        assert manager.image_name == "test:latest"

    def test_container_name_from_id(self):
        """Test container name generation from runtime ID"""
        manager = DockerRuntimeContainerManager(runtime_name_prefix="ohrt-")
        runtime_id = uuid4()
        expected_name = f"ohrt-{runtime_id}"
        assert manager._container_name_from_id(runtime_id) == expected_name

    def test_runtime_id_from_container_name(self):
        """Test runtime ID extraction from container name"""
        manager = DockerRuntimeContainerManager(runtime_name_prefix="ohrt-")
        runtime_id = uuid4()
        container_name = f"ohrt-{runtime_id}"
        
        extracted_id = manager._runtime_id_from_container_name(container_name)
        assert extracted_id == runtime_id

    def test_runtime_id_from_invalid_container_name(self):
        """Test runtime ID extraction from invalid container name"""
        manager = DockerRuntimeContainerManager(runtime_name_prefix="ohrt-")
        
        # Wrong prefix
        assert manager._runtime_id_from_container_name("wrong-prefix-123") is None
        
        # Invalid UUID
        assert manager._runtime_id_from_container_name("ohrt-invalid-uuid") is None

    def test_docker_status_to_runtime_status(self):
        """Test Docker status to RuntimeContainerStatus conversion"""
        manager = DockerRuntimeContainerManager()
        
        assert manager._docker_status_to_runtime_status("running") == RuntimeContainerStatus.RUNNING
        assert manager._docker_status_to_runtime_status("paused") == RuntimeContainerStatus.PAUSED
        assert manager._docker_status_to_runtime_status("exited") == RuntimeContainerStatus.PAUSED
        assert manager._docker_status_to_runtime_status("created") == RuntimeContainerStatus.STARTING
        assert manager._docker_status_to_runtime_status("dead") == RuntimeContainerStatus.ERROR
        assert manager._docker_status_to_runtime_status("unknown") == RuntimeContainerStatus.ERROR

    @patch('openhands_server.runtime.docker_runtime_manager.DockerClient')
    def test_container_to_runtime_containers(self, mock_docker_client):
        """Test container to RuntimeInfo conversion"""
        manager = DockerRuntimeContainerManager()
        
        # Mock container
        runtime_id = uuid4()
        user_id = uuid4()
        container_name = f"ohrt-{runtime_id}"
        
        mock_container = Mock()
        mock_container.name = container_name
        mock_container.status = "running"
        mock_container.labels = {"user_id": str(user_id)}
        mock_container.attrs = {
            "Created": "2023-01-01T12:00:00.000000Z"
        }
        
        runtime_containers = manager._container_to_runtime_containers(mock_container)
        
        assert runtime_containers is not None
        assert runtime_containers.id == runtime_id
        assert runtime_containers.user_id == user_id
        assert runtime_containers.status == RuntimeContainerStatus.RUNNING
        assert runtime_containers.url is not None  # Should have URL for running container

    @patch('openhands_server.runtime.docker_runtime_manager.DockerClient')
    def test_container_to_runtime_containers_invalid(self, mock_docker_client):
        """Test container to RuntimeInfo conversion with invalid data"""
        manager = DockerRuntimeContainerManager()
        
        # Mock container with invalid name
        mock_container = Mock()
        mock_container.name = "invalid-name"
        
        runtime_containers = manager._container_to_runtime_containers(mock_container)
        assert runtime_containers is None
        
        # Mock container without user_id label
        mock_container.name = "ohrt-" + str(uuid4())
        mock_container.labels = {}
        
        runtime_containers = manager._container_to_runtime_containers(mock_container)
        assert runtime_containers is None

    @pytest.mark.asyncio
    @patch('openhands_server.runtime.docker_runtime_manager.DockerClient')
    async def test_start_runtime(self, mock_docker_client):
        """Test starting a runtime"""
        mock_client = Mock()
        mock_docker_client.from_env.return_value = mock_client
        
        mock_container = Mock()
        mock_client.containers.run.return_value = mock_container
        
        manager = DockerRuntimeContainerManager(client=mock_client, image_name="test:latest")
        user_id = uuid4()
        
        runtime_id = await manager.start_runtime(user_id)
        
        assert runtime_id is not None
        mock_client.containers.run.assert_called_once()
        
        # Check the call arguments
        call_args = mock_client.containers.run.call_args
        assert call_args[0][0] == "test:latest"  # image name
        assert call_args[1]["labels"]["user_id"] == str(user_id)
        assert call_args[1]["detach"] is True

    @pytest.mark.asyncio
    @patch('openhands_server.runtime.docker_runtime_manager.DockerClient')
    async def test_get_runtime_containers_not_found(self, mock_docker_client):
        """Test getting runtime info for non-existent runtime"""
        from docker.errors import NotFound
        
        mock_client = Mock()
        mock_docker_client.from_env.return_value = mock_client
        mock_client.containers.get.side_effect = NotFound("Container not found")
        
        manager = DockerRuntimeContainerManager(client=mock_client)
        runtime_id = uuid4()
        
        result = await manager.get_runtime_containers(runtime_id)
        assert result is None

    @pytest.mark.asyncio
    @patch('openhands_server.runtime.docker_runtime_manager.DockerClient')
    async def test_delete_runtime(self, mock_docker_client):
        """Test deleting a runtime"""
        mock_client = Mock()
        mock_docker_client.from_env.return_value = mock_client
        
        mock_container = Mock()
        mock_container.status = "running"
        mock_client.containers.get.return_value = mock_container
        
        manager = DockerRuntimeContainerManager(client=mock_client)
        runtime_id = uuid4()
        
        result = await manager.delete_runtime(runtime_id)
        
        assert result is True
        mock_container.stop.assert_called_once()
        mock_container.remove.assert_called_once()

    @pytest.mark.asyncio
    @patch('openhands_server.runtime.docker_runtime_manager.DockerClient')
    async def test_delete_runtime_not_found(self, mock_docker_client):
        """Test deleting a non-existent runtime"""
        from docker.errors import NotFound
        
        mock_client = Mock()
        mock_docker_client.from_env.return_value = mock_client
        mock_client.containers.get.side_effect = NotFound("Container not found")
        
        manager = DockerRuntimeContainerManager(client=mock_client)
        runtime_id = uuid4()
        
        result = await manager.delete_runtime(runtime_id)
        assert result is False

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test using DockerRuntimeContainerManager as async context manager"""
        manager = DockerRuntimeContainerManager()
        
        async with manager as mgr:
            assert mgr is manager
        
        # Should not raise any exceptions