

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class RuntimeImageStatus(Enum):
    BUILDING = "BUILDING"
    READY = "READY"
    ERROR = "ERROR"
    DELETING = "DELETING"


class RuntimeImageInfo(BaseModel):
    """ A runtime image is a template for creating a runtime, analogous to a docker image """
    id: str
    image_name: str
    command: str
    created_at: datetime
    initial_env: dict[str, str] = Field(description="Initial Environment Variables")
    working_dir: str = '/openhands/code'


class RuntimeImageInfoPage(BaseModel):
    items: list[RuntimeImageInfo]
    next_page_id: str | None = None
