
from dataclasses import dataclass, field
import docker

from openhands_server.runtime_container.runtime_container_manager import RuntimeContainerManager
from openhands_server.runtime_image.docker_runtime_image_manager import DockerRuntimeImageManager


@dataclass
class VolumeMount:
    host_path: str
    container_path: str
    mode: str = 'rw'


@dataclass
class ExposedPort:
    """Exposed port. A free port will be found for this and an environment variable set"""
    name: str
    description: str


@dataclass
class DockerRuntimeContainerManager(RuntimeContainerManager):

    client: docker.DockerClient = field(default_factory=docker.from_env)
    container_name_prefix: str = "openhands-runtime-"
    runtime_image_manager: DockerRuntimeImageManager = field(default_factory=DockerRuntimeImageManager.get_instance)
    mounts: list[VolumeMount] = field(default_factory=list)
    exposed_port: list[ExposedPort] = field(default_factory=lambda: [
        ExposedPort("APPLICATION_SERVER_PORT", 'The port on which the application server runs within the container')
    ])
    exposed_url_pattern: str = "http://localhost:{port}"
