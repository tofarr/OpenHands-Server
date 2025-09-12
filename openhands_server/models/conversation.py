

from datetime import datetime
from uuid import UUID

from openhands_server.models.conversation_status import ConversationStatus
from openhands_server.models.runtime_status import RuntimeStatus
from pydantic import BaseModel, Field, ConfigDict


class Conversation(BaseModel):
    id: UUID
    runtime_id: UUID | None
    status: ConversationStatus
    created_at: datetime = Field(..., description="Timestamp when the conversation was created")
    updated_at: datetime = Field(..., description="Timestamp when the conversation was updated")
