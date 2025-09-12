
from dataclasses import dataclass, field
import docker

from openhands_server.runtime_container.runtime_container_manager import RuntimeContainerManager
from openhands_server.runtime_image.docker_runtime_image_manager import DockerRuntimeImageManager



@dataclass
class DockerRuntimeContainerManager(RuntimeContainerManager):

    client: docker.DockerClient = field(default_factory=docker.from_env)
    container_name_prefix: str = "openhands-runtime-"
    runtime_image_manager: DockerRuntimeImageManager = field(default_factory=DockerRuntimeImageManager.get_instance)
