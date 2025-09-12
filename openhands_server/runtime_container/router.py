"""Runtime Containers router for OpenHands Server."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from openhands import get_impl, get_user_id

from openhands_server.runtime_container.model import RuntimeContainerInfo, RuntimeContainerPage
from openhands_server.runtime_container.manager import RuntimeContainerManager
from openhands_server.utils.success import Success

router = APIRouter(prefix="/runtime-containers")
runtime_manager: RuntimeContainerManager = get_impl(RuntimeContainerManager)()
router.lifespan(runtime_manager)

# TODO: Currently a runtime container is only available to the user who created it. In future we could have a more advanced permissions model for sharing

# Read methods

@router.get("/search")
async def search_runtime_containers(page_id: str | None = None, limit: int = 100, user_id: UUID = Depends(get_user_id)) -> RuntimeContainerPage:
    assert limit > 0
    assert limit <= 100
    return await runtime_manager.search_runtime_containers(user_id, page_id, limit)


@router.get("/{id}")
async def get_runtime_containers(id: UUID, user_id: UUID = Depends(get_user_id)) -> RuntimeContainerInfo:
    runtime_containers = await runtime_manager.get_runtime_containers(id)
    if runtime_containers is None or runtime_containers.user_id != user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return runtime_containers


@router.get("/")
async def batch_get_runtimes(ids: list[UUID], user_id: UUID = Depends(get_user_id)) -> list[RuntimeContainerInfo | None]:
    assert len(ids) < 100
    runtime_containerss = await runtime_manager.batch_get_runtime_containers(user_id, ids)
    runtime_containerss = [
        runtime_containers if runtime_containers and runtime_containers.user_id == user_id else None
        for runtime_containers in runtime_containerss
    ]
    return runtime_containerss


# Write Methods

@router.post("/")
async def start_runtime(user_id: UUID = Depends(get_user_id)) -> UUID:
    id = await runtime_manager.start_runtime(user_id)
    return id


@router.post("/{id}/pause")
async def pause_runtime(id: UUID, user_id: UUID = Depends(get_user_id)) -> Success:
    exists = await runtime_manager.pause_runtime(user_id, id)
    if not exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND) 
    return Success()

@router.post("/{id}/resume")
async def resume_runtime(id: UUID, user_id: UUID = Depends(get_user_id)) -> Success:
    exists = await runtime_manager.resume_runtime(user_id, id)
    if not exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND) 
    return Success()


@router.delete("/{id}")
async def delete_runtime(id: UUID, user_id: UUID = Depends(get_user_id)) -> Success:
    exists = await runtime_manager.delete_runtime(user_id, id)
    if not exists:
        raise HTTPException(status.HTTP_404_NOT_FOUND) 
    return Success()