"""Runtimes router for OpenHands Server."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from openhands import get_impl, get_user_id

from openhands_server.runtime.page import RuntimeInfoPage
from openhands_server.runtime.runtime_info import RuntimeInfo
from openhands_server.runtime.runtime_manager import RuntimeManager
from openhands_server.utils.success import Success

router = APIRouter(prefix="/runtimes", tags=["runtimes"])
runtime_manager: RuntimeManager = get_impl(RuntimeManager)()
router.lifespan(runtime_manager)

# Read methods

@router.get("/search")
async def search_runtime_info(page_id: str | None = None, limit: int = 100, user_id: UUID = Depends(get_user_id)) -> RuntimeInfoPage:
    assert limit > 0
    assert limit <= 100
    return await runtime_manager.search_runtime_info(user_id, page_id, limit)


@router.get("/{id}")
async def get_runtime_info(id: UUID, user_id: UUID = Depends(get_user_id)) -> RuntimeInfo:
    runtime_info = await runtime_manager.get_runtime_info(id)
    if runtime_info is None or runtime_info.user_id != user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return runtime_info


@router.get("/")
async def batch_get_runtimes(ids: list[UUID], user_id: UUID = Depends(get_user_id)) -> list[RuntimeInfo | None]:
    assert len(ids) < 100
    runtime_infos = await runtime_manager.batch_get_runtime_info(user_id, ids)
    runtime_infos = [
        runtime_info if runtime_info and runtime_info.user_id == user_id else None
        for runtime_info in runtime_infos
    ]
    return runtime_infos


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