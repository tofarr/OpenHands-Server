

from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, SecretStr


class RuntimeStatus(Enum):
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


class RuntimeInfo(BaseModel):
    """Information about a runtime"""
    id: UUID
    user_id: UUID
    runtime_image_id: UUID
    status: RuntimeStatus
    url: str | None = Field(description="URL to access runtime. Runtimes with a status STARTING / PAUSED / DELETED / ERROR runtimes will not have a url")
    session_api_key: SecretStr | None = Field(description="URL to access runtime. Runtimes with a status STARTING / PAUSED / DELETED / ERROR runtimes will not have a key")
    created_at: datetime


class RuntimeInfoPage(BaseModel):
    items: list[RuntimeInfo]
    next_page_id: str | None = None
