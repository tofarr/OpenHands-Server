
from pydantic import BaseModel
from openhands_server.runtime.runtime_info import RuntimeInfo


class RuntimeInfoPage(BaseModel):
    items: list[RuntimeInfo]
    next_page_id: str
