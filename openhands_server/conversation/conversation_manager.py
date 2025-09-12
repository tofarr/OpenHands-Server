

from abc import ABC, abstractmethod
from uuid import UUID

from openhands_server.conversation.model import ConversationInfo, ConversationInfoPage


class ConversationManager(ABC):

    @abstractmethod
    async def search_conversation_info(user_id: UUID | None = None, page_id: str | None = None, limit: int = 100) -> ConversationInfoPage:
        """Search for conversations"""

    @abstractmethod
    async def get_conversation_info(id: UUID) -> ConversationInfo | None:
        """Get a single conversation info. Return None if the conversation was not found."""

    @abstractmethod
    async def batch_get_conversation_info(ids: list[UUID]) -> list[ConversationInfo | None]:
        """Get a batch of conversation info. Return None for any conversation which was not found."""

    @abstractmethod
    async def create_conversation(user_id: UUID, runtime_id: UUID, and_start: bool = True) -> UUID:
        """Begin the process of starting a conversation. Return the UUID of the new conversation """

    @abstractmethod
    async def stop_conversation(id: UUID) -> UUID:
        """Begin the process of starting a conversation. Return the UUID of the new conversation """

    @abstractmethod
    async def start_conversation(id: UUID) -> bool:
        """Begin the process of resuming a conversation. Return True if the conversation exists and is being resumed or is already running. Return False if the conversation did not exist"""

    @abstractmethod
    async def delete_conversation(id: UUID) -> bool:
        """Begin the process of deleting a conversation (Which may involve stopping it first). Return False if the conversation did not exist"""

    async def __aenter__():
        """Start using this conversation manager"""

    async def __aexit__():
        """Stop using this conversation manager"""