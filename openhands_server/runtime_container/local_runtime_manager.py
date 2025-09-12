import httpx

from openhands_server.runtime.model import RuntimeInfo
from openhands_server.runtime.runtime_manager import RuntimeContainerManager


class LocalRuntimeContainerManager(RuntimeContainerManager):
    """
    Runtime manager for starting / runtimes in the current process.
    """

    async def search_runtime_containers(user_id = None, page_id = None, limit = 100):
        raise NotImplementedError

    async def get_runtime_containers(id) -> RuntimeInfo | None:
        
        return RuntimeInfo(
            id=id,
            user_id=stored_runtime.user_id
        )

    async def batch_get_runtime_containers(ids):
        raise NotImplementedError

    async def start_runtime(user_id):
        raise NotImplementedError

    async def resume_runtime(id):
        raise NotImplementedError

    async def pause_runtime(id):
        raise NotImplementedError

    async def delete_runtime(id):
        httpx

        raise NotImplementedError
