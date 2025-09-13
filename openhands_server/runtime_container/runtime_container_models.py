

from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, SecretStr


class RuntimeContainerStatus(Enum):
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


class ExposedUrl(BaseModel):
    """ URL to access some named service within the container. """
    name: str
    url: str


class RuntimeContainerInfo(BaseModel):
    """Information about a runtime"""
    id: UUID
    user_id: str
    runtime_image_id: str
    status: RuntimeContainerStatus
    url: str | None = Field(description="URL to access runtime. Runtimes with a status STARTING / PAUSED / DELETED / ERROR runtimes will not have a url")
    session_api_key: SecretStr | None = Field(description="Key to access runtime, to be added as an `X-Session-API-Key` header in each request. Runtimes with a status STARTING / PAUSED / DELETED / ERROR runtimes will not have a key")
    exposed_urls: list[ExposedUrl]
    created_at: datetime


class RuntimeContainerPage(BaseModel):
    items: list[RuntimeContainerInfo]
    next_page_id: str | None = None
