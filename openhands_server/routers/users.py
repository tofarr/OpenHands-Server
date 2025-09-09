"""Users router for OpenHands Server."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models.user import User

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    """Schema for creating a user."""
    id: str
    language: str = "en"
    email: str
    is_admin: bool = False


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    language: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True


@router.get("/hello")
async def hello_users():
    """Hello world endpoint for users router."""
    return {"message": "Hello from Users router!", "router": "users"}


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.id == user.id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Create new user
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """Get all users."""
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}