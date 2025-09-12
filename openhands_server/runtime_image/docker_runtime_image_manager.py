

from dataclasses import dataclass, field
import docker
from openhands_server.runtime_image.runtime_image_manager import RuntimeImageManager


@dataclass
class DockerRuntimeImageManager(RuntimeImageManager):

    client: docker.DockerClient = field(default_factory=docker.from_env)
    image_name: str = "ubuntu:latest",

    async def search_runtime_image_info(user_id = None, page_id = None, limit = 100):
        raise NotImplementedError

    async def get_runtime_image_info(id):
        raise NotImplementedError

    async def batch_get_runtime_image_info(ids):
        raise NotImplementedError
