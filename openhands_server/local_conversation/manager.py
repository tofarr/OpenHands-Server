

from abc import ABC, abstractmethod
from uuid import UUID

from openhands_server.local_conversation.model import LocalConversationInfo, StartConversationRequest
from openhands_server.sandboxed_conversation.sandboxed_conversation_models import LocalConversationPage


class LocalConversationService(ABC):
    """
    Local conversations have no concept of a user - it is whoever has been granted access to
    the sandbox in which the conversation is being run.

    A local conversation service may simply run in the current environment, or it may run and pass events
    to another url or process.
    """

    async def search_local_conversations(self, user_id: UUID, page_id: str | None = None, limit: int = 100) -> SandboxedConversationPage:
        """Search for local conversations"""


    async def get_local_conversation(self, user_id: UUID, conversation_id: UUID) -> SandboxedConversationInfo:
        """Get a single local conversation info. Return None if the conversation was not found."""


    async def batch_get_local_conversations(self, conversation_ids: list[UUID]) -> list[SandboxedConversationInfo | None]:
        """Get a batch of local conversations. Return None for any conversation which was not found."""


    # Write Methods

    async def start_local_conversation(self, request: StartSandboxedConversationRequest) -> UUID:
        """ Start a local conversation and return its id. """

    async def pause_local_conversation(self, conversation_id: UUID) -> bool:
        """ Pause a local conversation. """

    async def resume_local_conversation(self, conversation_id: UUID) -> bool:
        """ Resume a local conversation. """

    async def delete_local_conversation(self, conversation_id: UUID) -> bool:
        """ Delete a local conversation. Stop it if it is running. """

    # Lifecycle methods

    async def __aenter__():
        """Start using this runtime image service"""

    async def __aexit__():
        """Stop using this runtime image service"""

    @classmethod
    @abstractmethod
    def get_instance(cls) -> "LocalConversationService":
        """ Get an instance of runtime image service """


_local_conversation_service = None


def get_default_local_conversation_service():
    global _local_conversation_service
    if _local_conversation_service:
        return _local_conversation_service
    _local_conversation_service = get_impl(LocalConversationService)
    return _local_conversation_service
