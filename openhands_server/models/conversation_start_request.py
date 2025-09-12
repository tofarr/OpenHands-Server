
from uuid import UUID
from openhands.sdk import Agent, Conversation, Message
from openhands.sdk.utils.async_utils import AsyncConversationCallback
from pydantic import BaseModel

from openhands_server.models.agent_request import AgentRequest


class ConversationStartRequest(BaseModel):
    runtime_id: UUID | None = None
    agent: AgentRequest
    initial_message: Message
    max_iteration_per_run: int = 500,

    def create_conversation(self, cwd: str, callback: AsyncConversationCallback) -> Conversation:
        agent = self.agent.create_agent(cwd)
        conversation = Conversation(agent=agent, callbacks=[callback])
        return conversation
