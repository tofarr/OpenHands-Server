
from docker import DockerClient
from openhands_server.runtime.runtime_manager import RuntimeManager


class DockerRuntimeManager(RuntimeManager):

    def __init__(
            self, 
            client: DockerClient | None = None,
            runtime_name_prefix: str = "ohrt-",
        ):
        self.client = client | DockerClient.from_env()
        self.runtime_name_prefix = runtime_name_prefix

    async def search_runtime_info(user_id = None, page_id = None, limit = 100):
        raise NotImplementedError

    async def get_runtime_info(id):
        raise NotImplementedError

    async def batch_get_runtime_info(ids):
        raise NotImplementedError

    async def start_runtime(user_id):
        raise NotImplementedError

    async def resume_runtime(id):
        raise NotImplementedError

    async def pause_runtime(id):
        raise NotImplementedError

    async def delete_runtime(id):
        raise NotImplementedError

        