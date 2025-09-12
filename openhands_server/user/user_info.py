
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """User model representing a user in the system."""
    id: UUID = Field(..., description="Unique identifier for the user")
    email: str | None = None
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(..., description="Timestamp when the user was updated")
    super_admin: bool = Field(default=False, description="Flag indicating if the user has super admin privileges")
    