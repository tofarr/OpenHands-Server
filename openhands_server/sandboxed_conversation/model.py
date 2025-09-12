

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class RuntimeConversationInfo(LocalConversationInfo):
    """Information about a conversation running remotely in a Runtime sandbox """
    runtime_container_id: UUID | None


class RuntimeConversationInfoPage(BaseModel):
    items: list[RuntimeConversationInfo]
    next_page_id: str | None = None
