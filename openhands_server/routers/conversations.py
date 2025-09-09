"""Conversations router for OpenHands Server."""

from fastapi import APIRouter

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("/hello")
async def hello_conversations():
    """Hello world endpoint for conversations router."""
    return {"message": "Hello from Conversations router!", "router": "conversations"}