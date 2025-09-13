"""Runtime Images router for OpenHands Server."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from openhands_server.runtime_image.runtime_image_models import RuntimeImageInfo, RuntimeImageInfoPage
from openhands_server.runtime_image.runtime_image_service import RuntimeImageService, get_default_runtime_image_service

router = APIRouter(prefix="/runtime-images")
runtime_image_service: RuntimeImageService = get_default_runtime_image_service()
router.lifespan(runtime_image_service)

# Read methods

@router.get("/search")
async def search_runtime_images(page_id: str | None = None, limit: int = 100) -> RuntimeImageInfoPage:
    assert limit > 0
    assert limit <= 100
    return await runtime_image_service.search_runtime_images(page_id=page_id, limit=limit)


@router.get("/{id}")
async def get_runtime_image(id: UUID) -> RuntimeImageInfo:
    runtime_images = await runtime_image_service.get_runtime_image(id)
    if runtime_images is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return runtime_images


@router.get("/")
async def batch_get_runtime_images(ids: list[UUID]) -> list[RuntimeImageInfo | None]:
    assert len(ids) <= 100
    runtime_imagess = await runtime_image_service.batch_get_runtime_images(ids)
    return runtime_imagess
