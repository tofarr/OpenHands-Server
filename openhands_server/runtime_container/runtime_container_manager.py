

from abc import ABC, abstractmethod
from uuid import UUID

from openhands_server.runtime_container.model import RuntimeContainerInfo, RuntimeContainerInfoPage


class RuntimeContainerManager(ABC):

    @abstractmethod
    async def search_runtime_containers(user_id: UUID | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeContainerInfoPage:
        """Search for runtime containers"""

    @abstractmethod
    async def get_runtime_containers(id: UUID) -> RuntimeContainerInfo | None:
        """Get a single runtime container info. Return None if the runtime container was not found."""

    @abstractmethod
    async def batch_get_runtime_containers(ids: list[UUID]) -> list[RuntimeContainerInfo | None]:
        """Get a batch of runtime container info. Return None for any runtime container which was not found."""

    @abstractmethod
    async def start_runtime_container(user_id: UUID) -> UUID:
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

    async def __aenter__():
        """Start using this runtime container manager"""

    async def __aexit__():
        """Stop using this runtime container manager"""