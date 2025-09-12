

from abc import ABC, abstractmethod
from uuid import UUID
# from openhands import get_impl  # Not available, using direct import instead
from openhands_server.runtime_image.model import RuntimeImageInfo, RuntimeImageInfoPage


class RuntimeImageManager(ABC):
    """
    Manager for runtime images. At present this is read only. The plan is that later this class will allow building
    and deleting runtime images and limiting access of images by user and group. It would also be nice to be able
    to set the desired number of warm containers for an image and scale this up and down.
    """

    @abstractmethod
    async def search_runtime_images(image_name__eq: str | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeImageInfoPage:
        """Search for runtimes"""

    @abstractmethod
    async def get_runtime_images(id: str) -> RuntimeImageInfo | None:
        """Get a single runtime info. Return None if the runtime was not found."""

    @abstractmethod
    async def batch_get_runtime_images(ids: list[str]) -> list[RuntimeImageInfo | None]:
        """Get a batch of runtime info. Return None for any runtime which was not found."""

    async def __aenter__():
        """Start using this runtime image manager"""

    async def __aexit__():
        """Stop using this runtime image manager"""

    @abstractmethod
    @classmethod
    def get_instance() -> "RuntimeImageManager":
        """ Get an instance of runtime image manager """


_runtime_image_manager = None


def get_default_runtime_image_manager():
    global _runtime_image_manager
    if _runtime_image_manager:
        return _runtime_image_manager
    # Import here to avoid circular imports
    from openhands_server.runtime_image.docker_runtime_image_manager import DockerRuntimeImageManager
    _runtime_image_manager = DockerRuntimeImageManager()
    return _runtime_image_manager
