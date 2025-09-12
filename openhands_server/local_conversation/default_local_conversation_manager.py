

from dataclasses import dataclass, field
import logging
import os
from pathlib import Path
from typing import Iterator
from uuid import UUID

from openhands_server.local_conversation.local_conversation import LocalConversation
from openhands_server.local_conversation.manager import LocalConversationManager
from openhands_server.local_conversation.model import LocalConversationInfo
from openhands_server.sandboxed_conversation.model import LocalConversationPage

from openhands.sdk import Conversation

logger = logging.getLogger(__name__)


@dataclass
class DefaultLocalConversationManager(LocalConversationManager):
    """ Conversation manager which stores to a local context. """

    conversations_path: Path = field(default=Path("/workspace/conversations"))
    _running_conversations: dict[UUID, LocalConversation] = field(default_factory=dict)

    async def search_local_conversations(self, page_id: str | None = None, limit: int = 100) -> LocalConversationPage:
        items = []
        for conversation_dir in self.conversations_path.iterdir():
            if page_id:
                if page_id != conversation_dir.name:
                    continue
                page_id = None
            try:
                if limit < 0:
                    return LocalConversationPage(items=items, next_page_id=conversation_dir.name)
                conversation_id = UUID(conversation_dir.name)
                conversation = self._running_conversations.get(conversation_id)
                if conversation:
                    yield conversation
                    continue
                json_str = (conversation_dir / "meta.json").read_text()
                conversation = LocalConversation.model_validate_json(json_str)
                yield conversation
            except Exception:
                logger.exception('error_reading_conversation:{conversation_dir}', stack_info=True)
        

    async def get_local_conversation(self, id: UUID) -> LocalConversationInfo:
        """Get a single local conversation info. Return None if the conversation was not found."""

    async def batch_get_local_conversations(self, ids: list[UUID]) -> list[LocalConversationInfo | None]:
        conversations = []
        for id in ids:
            try:
                conversation = await self.get_local_conversation(id)
                conversations.append(conversation)
            except Exception:
                conversations.append(None)
        return conversations

    # Write Methods

    async def start_local_conversation() -> UUID:
        """ Start a local conversation and return its id. """


    async def pause_local_conversation(id: UUID) -> bool:
        """ Pause a local conversation. """

    async def resume_local_conversation(id: UUID) -> bool:
        """ Resume a local conversation. """

    async def delete_local_conversation(id: UUID) -> bool:
        """ Delete a local conversation. Stop it if it is running. """
