"""Users router for OpenHands Server."""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/hello")
async def hello_users():
    """Hello world endpoint for users router."""
    return {"message": "Hello from Users router!", "router": "users"}