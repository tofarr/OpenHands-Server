"""User model for OpenHands Server."""

from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.declarative import declarative_base

from ..database import Base


class User(Base):
    """User entity for OpenHands Server.
    
    Attributes:
        id: Unique string identifier for the user
        language: User's preferred language (e.g., 'en', 'es', 'fr')
        email: User's email address
        is_admin: Flag indicating whether the user is a server admin
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    language = Column(String, nullable=False, default="en")
    email = Column(String, unique=True, index=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', is_admin={self.is_admin})>"