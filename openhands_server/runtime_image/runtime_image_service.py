

from abc import ABC, abstractmethod
from openhands_server.runtime_image.runtime_image_models import RuntimeImageInfo, RuntimeImageInfoPage
from openhands_server.utils.import_utils import get_impl


class RuntimeImageService(ABC):
    """
    Service for accessing for runtime images. At present this is read only. The plan is that later this class
    will allow building and deleting runtime images and limiting access of images by user and group.
    It would also be nice to be able to set the desired number of warm containers for an image and scale this
    up and down.
    """

    @abstractmethod
    async def search_runtime_images(image_name__eq: str | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeImageInfoPage:
        """Search for runtimes"""

    @abstractmethod
    async def get_runtime_image(id: str) -> RuntimeImageInfo | None:
        """Get a single runtime info. Return None if the runtime was not found."""

    @abstractmethod
    async def batch_get_runtime_images(ids: list[str]) -> list[RuntimeImageInfo | None]:
        """Get a batch of runtime info. Return None for any runtime which was not found."""

    # Lifecycle methods

    async def __aenter__():
        """Start using this runtime image service"""

    async def __aexit__():
        """Stop using this runtime image service"""

    @classmethod
    @abstractmethod
    def get_instance(cls) -> "RuntimeImageService":
        """ Get an instance of runtime image service """


_runtime_image_service = None


def get_default_runtime_image_service():
    global _runtime_image_service
    if _runtime_image_service:
        return _runtime_image_service
    _runtime_image_service = get_impl(RuntimeImageService)
    return _runtime_image_service
