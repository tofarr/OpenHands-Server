

from abc import ABC, abstractmethod
from uuid import UUID

from openhands_server.runtime.page import RuntimeInfoPage
from openhands_server.runtime.runtime_info import RuntimeInfo


class RuntimeManager(ABC):

    @abstractmethod
    async def search_runtime_info(user_id: UUID | None = None, page_id: str | None = None, limit: int = 100) -> RuntimeInfoPage:
        """Search for runtimes"""

    @abstractmethod
    async def get_runtime_info(id: UUID) -> RuntimeInfo | None:
        """Get a single runtime info. Return None if the runtime was not found."""

    @abstractmethod
    async def batch_get_runtime_info(ids: list[UUID]) -> list[RuntimeInfo | None]:
        """Get a batch of runtime info. Return None for any runtime which was not found."""

    @abstractmethod
    async def start_runtime(user_id: UUID) -> UUID:
        """Begin the process of starting a runtime. Return the UUID of the new runtime """

    @abstractmethod
    async def resume_runtime(id: UUID) -> bool:
        """Begin the process of resuming a runtime. Return True if the runtime exists and is being resumed or is already running. Return False if the runtime did not exist"""

    @abstractmethod
    async def pause_runtime(id: UUID) -> bool:
        """Begin the process of deleting a runtime. Return True if the runtime exists and is being paused or is already paused. Return False if the runtime did not exist"""

    @abstractmethod
    async def delete_runtime(id: UUID) -> bool:
        """Begin the process of deleting a runtime (Which may involve stopping it first). Return False if the runtime did not exist"""

    async def __aenter__():
        """Start using this runtime manager"""

    async def __aexit__():
        """Stop using this runtime manager"""