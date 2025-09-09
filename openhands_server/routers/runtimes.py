"""Runtimes router for OpenHands Server."""

from fastapi import APIRouter

router = APIRouter(prefix="/runtimes", tags=["runtimes"])


@router.get("/hello")
async def hello_runtimes():
    """Hello world endpoint for runtimes router."""
    return {"message": "Hello from Runtimes router!", "router": "runtimes"}