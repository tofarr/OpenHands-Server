

from dataclasses import dataclass, field
from datetime import UTC, datetime
import logging
from mailbox import Message
import os
from pathlib import Path
import shutil
from uuid import UUID, uuid4

from openhands_server.local_conversation.local_conversation import LocalConversation
from openhands_server.local_conversation.service import LocalConversationService
from openhands_server.local_conversation.model import LocalConversationInfo, LocalConversationPage, StartConversationRequest, StoredLocalConversation


logger = logging.getLogger(__name__)


@dataclass
class DefaultLocalConversationService(LocalConversationService):
    """ Conversation service which stores to a local context. """

    file_store_path: Path = field(default=Path("/workspace/conversations"))
    workspace_path: Path = field(default=Path("/workspace"))
    _running_conversations: dict[UUID, LocalConversation] = field(default_factory=dict)

    async def get_local_conversation(self, conversation_id: UUID) -> LocalConversationInfo:
        conversation = self._running_conversations.get(id)
        if conversation is not None:
            status = await conversation.get_status()
            return LocalConversationInfo(**conversation.stored.model_dump(), status=status)
        
        meta_file = self.file_store_path / conversation_id.hex / "meta.json"
        json_str = meta_file.read_text()
        # This works because the only field defined is status which defaults to stopped
        conversation = LocalConversationInfo.model_validate_json(json_str)
        return conversation
    
    async def search_local_conversations(self, page_id: str | None = None, limit: int = 100) -> LocalConversationPage:
        items = []
        for conversation_dir in self.file_store_path.iterdir():
            if page_id:
                if page_id != conversation_dir.name:
                    continue
                page_id = None
            try:
                if limit < 0:
                    return LocalConversationPage(items=items, next_page_id=conversation_dir.name)
                conversation_id = UUID(conversation_dir.name)
                conversation = self.get_local_conversation(conversation_id)
                items.append(conversation)
            except Exception:
                logger.exception('error_reading_conversation:{conversation_dir}', stack_info=True)
        return LocalConversationPage(items=items)

    async def batch_get_local_conversations(self, conversation_ids: list[UUID]) -> list[LocalConversationInfo | None]:
        conversations = []
        for conversation_id in conversation_ids:
            try:
                conversation = await self.get_local_conversation(conversation_id)
                conversations.append(conversation)
            except Exception:
                conversations.append(None)
        return conversations

    # Write Methods

    async def start_local_conversation(self, request: StartConversationRequest) -> UUID:
        """ Start a local conversation and return its id. """
        conversation_id = uuid4(),
        stored = StoredLocalConversation(id=conversation_id, **request.model_dump())
        conversation = LocalConversation(
            stored=stored,
            file_store_path=self.file_store_path / conversation_id.hex / "conversation",
            working_dir=self.workspace_path / conversation_id.hex,
        )
        conversation.subscribe(_EventListener(self, conversation_id))
        self._running_conversations[id] = conversation
        return id

    async def pause_local_conversation(self, conversation_id: UUID) -> bool:
        conversation = self._running_conversations.get(conversation_id)
        await conversation.pause()

    async def resume_local_conversation(self, conversation_id: UUID) -> bool:
        conversation = self._running_conversations.get(conversation_id)
        await conversation.start()

    async def delete_local_conversation(self, conversation_id: UUID) -> bool:
        conversation = self._running_conversations.pop(conversation_id)
        if conversation:
            await conversation.close()
        shutil.rmtree(self.file_store_path / conversation_id.hex)
        shutil.rmtree(self.workspace_path / conversation_id.hex)

    @classmethod
    def get_instance(cls) -> LocalConversationService:
        return DefaultLocalConversationService()


@dataclass
class _EventListener:
    conversation: LocalConversation

    async def __call__(self, message: Message):
        # Saving also updates the updated_at timestamp
        self.conversation.save()
