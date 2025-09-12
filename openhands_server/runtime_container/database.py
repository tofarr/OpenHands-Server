
from uuid import UUID
from openhands import Base
from sqlalchemy import Column, UUID, DateTime


class StoredRuntimeInfo(Base):
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
