
from dataclasses import dataclass, field
import docker
from openhands_server.runtime_image.runtime_image_manager import RuntimeImageManager


@dataclass
class DockerRuntimeImageManager(RuntimeImageManager):
    """Runtime manager for docker images. By default, all images with the name given are loaded and returned (They may have different ta)"""

    client: docker.DockerClient = field(default_factory=docker.from_env)
    repository: str = "ghcr.io/all-hands-ai/runtime"
    command: str = "python -u -m openhands_server.runtime"
    initial_env: dict[str, str] = field(default_factory=dict)
    exposed_ports: dict[int, str] = field(default_factory=dict, description="Exposed ports to be mapped to endpoint urls in the resulting container")
    working_dir: str = '/openhands/code'

    async def search_runtime_image_info(image_name__eq = None, page_id = None, limit = 100):
        raise NotImplementedError

    async def get_runtime_image_info(id):
        raise NotImplementedError

    async def batch_get_runtime_image_info(ids):
        raise NotImplementedError
