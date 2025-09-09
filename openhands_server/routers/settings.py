"""Settings router for OpenHands Server."""

from fastapi import APIRouter

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/hello")
async def hello_settings():
    """Hello world endpoint for settings router."""
    return {"message": "Hello from Settings router!", "router": "settings"}