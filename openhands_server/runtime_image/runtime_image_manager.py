

from abc import ABC, abstractmethod
from uuid import UUID

from openhands_server.runtime_image.model import RuntimeImageInfo, RuntimeImageInfoPage


class RuntimeImageManager(ABC):

    @abstractmethod
    async def search_runtime_image_info(user_id: UUID | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeImageInfoPage:
        """Search for runtimes"""

    @abstractmethod
    async def get_runtime_image_info(id: UUID) -> RuntimeImageInfo | None:
        """Get a single runtime info. Return None if the runtime was not found."""

    @abstractmethod
    async def batch_get_runtime_image_info(ids: list[UUID]) -> list[RuntimeImageInfo | None]:
        """Get a batch of runtime info. Return None for any runtime which was not found."""

    async def __aenter__():
        """Start using this runtime image manager"""

    async def __aexit__():
        """Stop using this runtime image manager"""


class MutableRuntimeImageManager(RuntimeImageManager, ABC):

    @abstractmethod
    async def build_runtime_image(user_id: UUID, target_num_warm_containers: int = 0) -> UUID:
        """Begin the process of building a runtime image. Return the UUID of the new runtime image """

    @abstractmethod
    async def update_target_num_warm_containers(id: UUID, target_num_warm_containers: int = 0) -> UUID:
        """Begin the process of building a runtime image. Return the UUID of the new runtime image """

    @abstractmethod
    async def delete_runtime_image(id: UUID) -> bool:
        """Begin the process of deleting a runtime image (Which may involve stopping any associated containers first). Return False if the runtime did not exist"""
