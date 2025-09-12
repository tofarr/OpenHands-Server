"""Runtimes router for OpenHands Server."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from openhands import get_user_id

from openhands_server.runtime_image.model import RuntimeImageInfo, RuntimeImageInfoPage
from openhands_server.runtime_image.runtime_image_manager import RuntimeImageManager, get_default_runtime_image_manager
from openhands_server.utils.success import Success

router = APIRouter(prefix="/runtime-images")
runtime_image_manager: RuntimeImageManager = get_default_runtime_image_manager()
router.lifespan(runtime_image_manager)

# Read methods

@router.get("/search")
async def search_runtime_image_info(page_id: str | None = None, limit: int = 100) -> RuntimeImageInfoPage:
    assert limit > 0
    assert limit <= 100
    return await runtime_image_manager.search_runtime_image_info(page_id=page_id, limit=limit)


@router.get("/{id}")
async def get_runtime_image_info(id: UUID) -> RuntimeImageInfo:
    runtime_image_info = await runtime_image_manager.get_runtime_image_info(id)
    if runtime_image_info is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return runtime_image_info


@router.get("/")
async def batch_get_runtime_image_info(ids: list[UUID]) -> list[RuntimeImageInfo | None]:
    assert len(ids) <= 100
    runtime_image_infos = await runtime_image_manager.batch_get_runtime_image_info(ids)
    return runtime_image_infos
