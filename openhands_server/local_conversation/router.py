"""Local Conversation router for OpenHands Server."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from openhands import get_impl, get_user_id

from openhands_server.local_conversation.service import LocalConversationService
from openhands_server.local_conversation.model import LocalConversationInfo, LocalConversationPage
from openhands_server.utils.success import Success

router = APIRouter(prefix="/local-conversations")
local_conversation_service: LocalConversationService = get_impl(LocalConversationService)()
router.lifespan(local_conversation_service)

# LocalConversations are not available in the outer nesting container. They do not currently have permissions
# as all validation is through the session_api_key

# Read methods

@router.get("/search")
async def search_local_conversations(page_id: str | None = None, limit: int = 100) -> LocalConversationPage:
    assert limit > 0
    assert limit <= 100
    return await local_conversation_service.search_local_conversations(page_id, limit)


@router.get("/{id}")
async def get_local_conversation(id: UUID) -> LocalConversationInfo:
    local_conversation = await local_conversation_service.get_local_conversation(conversation_id)
    if local_conversation is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return local_conversation


@router.get("/")
async def batch_get_local_conversations(ids: list[UUID]) -> list[LocalConversationInfo | None]:
    assert len(ids) < 100
    local_conversations = await local_conversation_service.batch_get_local_conversations(ids)
    return local_conversations


# Write Methods

@router.post("/")
async def start_local_conversation() -> UUID:
    id = await local_conversation_service.start_local_conversation()
    return id


@router.post("/{id}/pause")
async def pause_local_conversation(id: UUID) -> Success:
    paused = await local_conversation_service.pause_local_conversation(id)
    if not paused:
        raise HTTPException(status.HTTP_400_BAD_REQUEST) 
    return Success()

@router.post("/{id}/resume")
async def resume_local_conversation(id: UUID) -> Success:
    paused = await local_conversation_service.resume_local_conversation(id)
    if not paused:
        raise HTTPException(status.HTTP_400_BAD_REQUEST) 
    return Success()


@router.delete("/{id}")
async def delete_local_conversation(id: UUID) -> Success:
    deleted = await local_conversation_service.delete_local_conversation(id)
    if not deleted:
        raise HTTPException(status.HTTP_400_BAD_REQUEST) 
    return Success()
