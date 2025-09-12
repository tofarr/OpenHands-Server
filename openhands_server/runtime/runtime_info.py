

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, SecretStr
from openhands_server.runtime.runtime_status import RuntimeStatus


class RuntimeInfo(BaseModel):
    """Information about a runtime"""
    id: UUID
    user_id: UUID
    status: RuntimeStatus
    url: str | None = Field(description="URL to access runtime. Runtimes with a status STARTING / PAUSED / DELETED / ERROR runtimes will not have a url")
    session_api_key: SecretStr | None = Field(description="URL to access runtime. Runtimes with a status STARTING / PAUSED / DELETED / ERROR runtimes will not have a key")
    created_at: datetime
