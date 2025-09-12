

import asyncio
from dataclasses import dataclass
from uuid import UUID

from fastapi import Path

from openhands.sdk import Conversation, LocalFileStore, Message
from openhands.sdk.utils.async_utils import AsyncCallbackWrapper, AsyncConversationCallback
from pydantic import BaseModel, PrivateAttr

from openhands_server.local_conversation.agent_request import AgentRequest
from openhands_server.local_conversation.model import ConversationStatus, LocalConversationInfo
from openhands_server.utils.pub_sub import PubSub



class LocalConversation(BaseModel):
    id: UUID
    # TODO: We need the status to set this.
    title: str | None
    agent: AgentRequest
    cwd: str
    file_store_path: str
    _lock: asyncio.Lock = PrivateAttr(default_factory=asyncio.Lock)
    _conversation: Conversation | None = PrivateAttr(default=None)
    _pub_sub: PubSub = PrivateAttr(default_factory=PubSub)

    async def start(self):
        async with self._lock:
            if self._conversation:
                with self._conversation.state as state:
                    # Agent has finished
                    if state.agent_finished:
                        return
                    
                    # Agent is already running
                    if not state.agent_paused and not state.agent_waiting_for_confirmation:
                        return

                self._conversation.run()
            
            agent = self.agent.create_agent(self.cwd)
            conversation = Conversation(
                agent=agent, 
                callbacks=[AsyncCallbackWrapper(self._pubsub)],
                persist_filestore=LocalFileStore(self.file_store_path))
            self._conversation = conversation
            loop = asyncio.get_running_loop()
            asyncio.create_task(loop.run_in_executor(None, conversation.run))

    async def pause(self):
        async with self._lock:
            if self._conversation:
                loop = asyncio.get_running_loop()
                asyncio.create_task(loop.run_in_executor(None, self._conversation.pause))

    async def close(self):
         async with self._lock:
            if self._conversation:
                loop = asyncio.get_running_loop()
                asyncio.create_task(loop.run_in_executor(None, self._conversation.close))

    async def get_info(self) -> LocalConversationInfo:
        async with self._lock:
            return LocalConversationInfo(
                id=self.id,
                title=self.title,
                status=await self.get_status(),
                created_at=self.created_at,
                updated_at=self.updated_at,
            )
        
    async def send_message(self, message: Message):
        async with self._lock:
            loop = asyncio.get_running_loop()
            asyncio.create_task(loop.run_in_executor(None, self._conversation.send_message, message))

    def subscribe(self, callback: AsyncConversationCallback) -> UUID:
        return self._pub_sub.subscribe(callback)

    def unsubscribe(self, callback_id: UUID) -> bool:
        return self._pub_sub.unsubscribe(callback_id)

    async def get_status(self) -> ConversationStatus:
        async with self._lock:
            if not self._conversation:
                return ConversationStatus.STOPPED
            with self._conversation.state as state:
                if state.agent_paused:
                    return ConversationStatus.PAUSED
                if state.agent_finished:
                    return ConversationStatus.FINISHED
            return ConversationStatus.RUNNING
