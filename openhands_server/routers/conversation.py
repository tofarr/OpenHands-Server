"""Conversations router for OpenHands Server."""

import asyncio
import os
from uuid import UUID
from fastapi import APIRouter

from openhands.sdk.utils.async_utils import AsyncCallbackWrapper
from openhands_server.models.conversation_start_request import ConversationStartRequest
from openhands_server.utils.conversation_executor import ConversationExecutor
from openhands_server.utils.pub_sub import PubSub

router = APIRouter(prefix="/conversation", tags=["conversations"])
cwd = os.getenv('WORKING_DIR', '/workspace')

# Read methods

@router.get("/search")
async def search_conversations():
    raise NotImplementedError()


@router.get("/{id}")
async def get_conversation(id: UUID):
    pass


@router.get("/")
async def batch_get_conversations(ids: list[UUID]):
    raise NotImplementedError()


# Write Methods

@router.post("/")
async def start_conversation(request: ConversationStartRequest):
    if request.runtime_id:
        # Start a conversation inside a nested runtime.
        raise NotImplementedError()
    
    pubsub = PubSub()
    conversation = request.create_conversation(cwd, [AsyncCallbackWrapper(pubsub)])
    conversation_executor = ConversationExecutor(conversation, pubsub)
    asyncio.create_task(conversation_executor.run_async)


@router.post("/pause/{id}")
async def pause_conversation(id: UUID):
    raise NotImplementedError()


@router.delete("/{id}")
async def delete_conversation(id: UUID):
    # Delete a nested conversation
    raise NotImplementedError()    
