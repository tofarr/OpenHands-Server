
from dataclasses import dataclass, field
import docker

from openhands_server.runtime_container.runtime_container_manager import RuntimeContainerManager



@dataclass
class DockerRuntimeContainerManager(RuntimeContainerManager):

    client: docker.DockerClient = field(default_factory=docker.from_env)
    container_name_prefix: str = "openhands-runtime-"

