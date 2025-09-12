
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import docker
from docker.errors import NotFound, APIError
from openhands_server.runtime_image.runtime_image_manager import RuntimeImageManager
from openhands_server.runtime_image.model import RuntimeImageInfo, RuntimeImageInfoPage, RuntimeImageStatus


@dataclass
class DockerRuntimeImageManager(RuntimeImageManager):

    client: docker.DockerClient = field(default_factory=docker.from_env)

    async def search_runtime_image_info(image_name__eq = None, page_id = None, limit = 100):
        raise NotImplementedError

    async def get_runtime_image_info(id):
        raise NotImplementedError

    async def batch_get_runtime_image_info(ids):
        raise NotImplementedError
