

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ConversationStatus(Enum):
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    STOPPED = 'STOPPED'
    ERROR = 'ERROR'


class ConversationInfo(BaseModel):
    id: UUID
    runtime_container_id: UUID | None
    status: ConversationStatus
    created_at: datetime = Field(..., description="Timestamp when the conversation was created")
    updated_at: datetime = Field(..., description="Timestamp when the conversation was updated")
    


class ConversationInfoPage(BaseModel):
    items: list[ConversationInfo]
    next_page_id: str
