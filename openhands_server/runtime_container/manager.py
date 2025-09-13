

from abc import ABC, abstractmethod
from uuid import UUID

from openhands_server.runtime_container.model import RuntimeContainerInfo, RuntimeContainerPage


class RuntimeContainerManager(ABC):

    @abstractmethod
    async def search_runtime_containers(user_id: UUID | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeContainerPage:
        """Search for runtime containers"""

    @abstractmethod
    async def get_runtime_containers(id: UUID) -> RuntimeContainerInfo | None:
        """Get a single runtime container info. Return None if the runtime container was not found."""

    @abstractmethod
    async def batch_get_runtime_containers(ids: list[UUID]) -> list[RuntimeContainerInfo | None]:
        """Get a batch of runtime container info. Return None for any runtime container which was not found."""

    @abstractmethod
    async def start_runtime_container(user_id: UUID, runtime_image_id: str) -> UUID:
        """Begin the process of starting a runtime. Return the UUID of the new runtime """

    @abstractmethod
    async def resume_runtime_container(id: UUID) -> bool:
        """Begin the process of resuming a runtime. Return True if the runtime exists and is being resumed or is already running. Return False if the runtime did not exist"""

    @abstractmethod
    async def pause_runtime_container(id: UUID) -> bool:
        """Begin the process of deleting a runtime. Return True if the runtime exists and is being paused or is already paused. Return False if the runtime did not exist"""

    @abstractmethod
    async def delete_runtime_container(id: UUID) -> bool:
        """Begin the process of deleting a runtime (Which may involve stopping it first). Return False if the runtime did not exist"""

    # Lifecycle methods

    async def __aenter__():
        """Start using this runtime container manager"""

    async def __aexit__():
        """Stop using this runtime container manager"""

    @classmethod
    @abstractmethod
    def get_instance(cls) -> "RuntimeContainerManager":
        """ Get an instance of runtime container manager """


_runtime_container_manager = None


def get_default_runtime_container_manager():
    global _runtime_container_manager
    if _runtime_container_manager:
        return _runtime_container_manager
    _runtime_container_manager = get_impl(RuntimeContainerManager)
    return _runtime_container_manager
