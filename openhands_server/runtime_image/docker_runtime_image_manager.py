
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import docker
from docker.errors import NotFound, APIError
from openhands_server.runtime_image.runtime_image_manager import RuntimeImageManager
from openhands_server.runtime_image.model import RuntimeImageInfo, RuntimeImageInfoPage


@dataclass
class DockerRuntimeImageManager(RuntimeImageManager):
    """
    Runtime manager for docker images. By default, all images with the repository given are loaded and returned (They may have different tag)
    The combination of the repository and tag is treated as the id in the resulting image.
    """

    client: docker.DockerClient = field(default_factory=docker.from_env)
    repository: str = "ghcr.io/all-hands-ai/runtime"
    command: str = "python -u -m openhands_server.runtime"
    initial_env: dict[str, str] = field(default_factory=dict)
    exposed_ports: dict[int, str] = field(default_factory=dict, description="Exposed ports to be mapped to endpoint urls in the resulting container")
    working_dir: str = '/openhands/code'

    def _docker_image_to_runtime_image_info(self, image) -> RuntimeImageInfo:
        """Convert a Docker image to RuntimeImageInfo"""
        # Extract repository and tag from image tags
        # Use the first tag if multiple tags exist, or use the image ID if no tags
        if image.tags:
            image_id = image.tags[0]  # Use repository:tag as ID
        else:
            image_id = image.id[:12]  # Use short image ID if no tags
        
        # Parse creation time from image attributes
        created_str = image.attrs.get('Created', '')
        try:
            # Docker timestamps are in ISO format
            created_at = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            created_at = datetime.now()
        
        return RuntimeImageInfo(
            id=image_id,
            command=self.command,
            created_at=created_at,
            initial_env=self.initial_env,
            exposed_ports=self.exposed_ports,
            working_dir=self.working_dir
        )

    async def search_runtime_image_info(self, image_name__eq: str | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeImageInfoPage:
        """Search for runtime images"""
        try:
            # If image_name__eq is provided, search for that specific image
            # Otherwise, search for all images with the configured repository
            if image_name__eq:
                search_name = image_name__eq
            else:
                search_name = self.repository
            
            # Get all images that match the repository
            images = self.client.images.list(name=search_name)
            
            # Convert Docker images to RuntimeImageInfo
            runtime_images = []
            for image in images:
                # Only include images that have tags matching our repository
                if image.tags:
                    for tag in image.tags:
                        if tag.startswith(self.repository):
                            runtime_images.append(self._docker_image_to_runtime_image_info(image))
                            break  # Only add once per image, even if multiple matching tags
            
            # Apply pagination
            start_idx = 0
            if page_id:
                try:
                    start_idx = int(page_id)
                except ValueError:
                    start_idx = 0
            
            end_idx = start_idx + limit
            paginated_images = runtime_images[start_idx:end_idx]
            
            # Determine next page ID
            next_page_id = None
            if end_idx < len(runtime_images):
                next_page_id = str(end_idx)
            
            return RuntimeImageInfoPage(
                items=paginated_images,
                next_page_id=next_page_id
            )
            
        except APIError as e:
            # Return empty page if there's an API error
            return RuntimeImageInfoPage(items=[], next_page_id=None)

    async def get_runtime_image_info(self, id: str) -> RuntimeImageInfo | None:
        """Get a single runtime image info by ID"""
        try:
            # Try to get the image by ID (which should be repository:tag)
            image = self.client.images.get(id)
            return self._docker_image_to_runtime_image_info(image)
        except (NotFound, APIError):
            return None

    async def batch_get_runtime_image_info(self, ids: list[str]) -> list[RuntimeImageInfo | None]:
        """Get a batch of runtime image info"""
        results = []
        for image_id in ids:
            result = await self.get_runtime_image_info(image_id)
            results.append(result)
        return results
