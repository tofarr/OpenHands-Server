

from dataclasses import Field
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class RuntimeImageStatus(Enum):
    BUILDING = "BUILDING"
    READY = "READY"
    ERROR = "ERROR"
    DELETING = "DELETING"


class RuntimeImageInfo(BaseModel):
    """ A runtime image is a template for creating a runtime, analogous to a docker image """
    id: UUID
    # user_id: UUID - Leaving this out of scope for now - eventually it would be nice to have permissions associated with runtime images
    image_name: str
    command: str
    created_at: datetime
    initial_env: dict[str, str] = Field(description="Initial Environment Variables")
    working_dir: str = '/openhands/code'
    num_warm_containers: int = Field(default=0, description="The number of containers to keep warm for this image")
    target_num_warm_containers: int = Field(default=0, description="The target number of containers to keep warm for this image")


class RuntimeImageInfoPage:
    items: list[RuntimeImageInfo]
    next_page_id: str | None = None
