import httpx

from openhands_server.runtime.model import RuntimeInfo
from openhands_server.runtime.runtime_manager import RuntimeManager


class LocalRuntimeManager(RuntimeManager):
    """
    Runtime manager for starting / runtimes in the current process.
    """

    async def search_runtime_info(user_id = None, page_id = None, limit = 100):
        raise NotImplementedError

    async def get_runtime_info(id) -> RuntimeInfo | None:
        
        return RuntimeInfo(
            id=id,
            user_id=stored_runtime.user_id
        )

    async def batch_get_runtime_info(ids):
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
