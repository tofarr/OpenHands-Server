
from datetime import datetime
from uuid import UUID
from openhands_server.runtime.runtime_status import RuntimeContainerStatus
from pydantic import BaseModel, Field, ConfigDict


class Runtime(BaseModel):
    id: UUID
    status: RuntimeContainerStatus
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(..., description="Timestamp when the user was updated")
