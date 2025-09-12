

from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field


# TODO: Review these status with Calvin & Xingyao
class ConversationStatus(Enum):
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    FINISHED = 'FINISHED'
    STOPPED = 'STOPPED'


class LocalConversationInfo(BaseModel):
    """ Information about a conversation running locally without a Runtime sandbox. """
    id: UUID
    title: str | None
    status: ConversationStatus
    created_at: datetime = Field(..., description="Timestamp when the conversation was created")
    updated_at: datetime = Field(..., description="Timestamp when the conversation was updated")


class LocalConversationPage(BaseModel):
    items: list[LocalConversationInfo]
    next_page_id: str | None = None
