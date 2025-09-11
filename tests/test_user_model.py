"""Tests for the User model."""

from datetime import datetime
import pytest
from openhands_server.models.user import User


def test_user_model_creation():
    """Test creating a User model instance."""
    user_id = "user_123"
    created_at = datetime.now()
    super_admin = True
    
    user = User(
        id=user_id,
        created_at=created_at,
        super_admin=super_admin
    )
    
    assert user.id == user_id
    assert user.created_at == created_at
    assert user.super_admin == super_admin


def test_user_model_default_super_admin():
    """Test that super_admin defaults to False."""
    user = User(
        id="user_456",
        created_at=datetime.now()
    )
    
    assert user.super_admin is False


def test_user_model_json_serialization():
    """Test JSON serialization of User model."""
    user = User(
        id="user_789",
        created_at=datetime(2023, 1, 1, 12, 0, 0),
        super_admin=True
    )
    
    json_data = user.model_dump_json()
    assert '"id":"user_789"' in json_data
    assert '"created_at":"2023-01-01T12:00:00"' in json_data
    assert '"super_admin":true' in json_data


def test_user_model_dict_serialization():
    """Test dictionary serialization of User model."""
    created_at = datetime(2023, 1, 1, 12, 0, 0)
    user = User(
        id="user_abc",
        created_at=created_at,
        super_admin=False
    )
    
    user_dict = user.model_dump()
    expected = {
        "id": "user_abc",
        "created_at": created_at,
        "super_admin": False
    }
    
    assert user_dict == expected


def test_user_model_validation():
    """Test User model field validation."""
    # Test missing required fields
    with pytest.raises(ValueError):
        User()
    
    with pytest.raises(ValueError):
        User(id="test")
    
    # Test valid creation
    user = User(id="test", created_at=datetime.now())
    assert user.id == "test"
    assert user.super_admin is False