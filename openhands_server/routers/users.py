"""Users router for OpenHands Server."""

from datetime import datetime
from fastapi import APIRouter
from typing import List

from ..models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
async def get_users():
    """Get all users."""
    # This is a placeholder implementation
    # In a real application, you would fetch users from a database
    sample_users = [
        User(
            id="user_001",
            created_at=datetime.now(),
            super_admin=True
        ),
        User(
            id="user_002", 
            created_at=datetime.now(),
            super_admin=False
        )
    ]
    return sample_users


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a specific user by ID."""
    # This is a placeholder implementation
    # In a real application, you would fetch the user from a database
    return User(
        id=user_id,
        created_at=datetime.now(),
        super_admin=False
    )