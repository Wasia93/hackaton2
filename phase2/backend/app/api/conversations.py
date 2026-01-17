"""
Conversations API Endpoint
Task: T-023 - Add conversation history loading

Handles conversation listing and message history retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
from sqlmodel import Session
from app.core.database import get_session
from app.core.auth import get_current_user_id
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


class ConversationResponse(BaseModel):
    """Response body for a conversation."""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = None


class ConversationsListResponse(BaseModel):
    """Response body for listing conversations."""
    conversations: List[ConversationResponse]
    total: int


class MessageResponse(BaseModel):
    """Response body for a message."""
    id: int
    role: str
    content: str
    tool_calls: Optional[Any] = None
    created_at: datetime


class ConversationMessagesResponse(BaseModel):
    """Response body for conversation messages."""
    conversation_id: int
    title: str
    messages: List[MessageResponse]
    total: int


@router.get("", response_model=ConversationsListResponse)
async def list_conversations(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    List all conversations for the current user.

    Returns conversations ordered by most recently updated.

    Args:
        user_id: Authenticated user's ID (from JWT)
        session: Database session

    Returns:
        ConversationsListResponse with list of conversations
    """
    conv_service = ConversationService(session, user_id)
    msg_service = MessageService(session)

    conversations = conv_service.get_all_conversations()

    response_items = []
    for conv in conversations:
        message_count = msg_service.get_message_count(conv.id)
        response_items.append(ConversationResponse(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=message_count
        ))

    return ConversationsListResponse(
        conversations=response_items,
        total=len(response_items)
    )


@router.get("/{conversation_id}", response_model=ConversationMessagesResponse)
async def get_conversation_messages(
    conversation_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all messages for a specific conversation.

    Args:
        conversation_id: ID of the conversation
        user_id: Authenticated user's ID (from JWT)
        session: Database session

    Returns:
        ConversationMessagesResponse with conversation details and messages

    Raises:
        HTTPException 404: If conversation not found or not owned by user
    """
    conv_service = ConversationService(session, user_id)
    msg_service = MessageService(session)

    # Verify conversation exists and belongs to user
    conversation = conv_service.get_conversation_by_id(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found"
        )

    # Get messages
    messages = msg_service.get_conversation_messages(conversation_id)

    return ConversationMessagesResponse(
        conversation_id=conversation.id,
        title=conversation.title,
        messages=[
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                tool_calls=msg.tool_calls,
                created_at=msg.created_at
            )
            for msg in messages
        ],
        total=len(messages)
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a conversation and all its messages.

    Args:
        conversation_id: ID of the conversation to delete
        user_id: Authenticated user's ID (from JWT)
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException 404: If conversation not found or not owned by user
    """
    conv_service = ConversationService(session, user_id)

    deleted = conv_service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found"
        )

    return {"message": f"Conversation {conversation_id} deleted successfully"}


@router.patch("/{conversation_id}/title")
async def update_conversation_title(
    conversation_id: int,
    title: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a conversation's title.

    Args:
        conversation_id: ID of the conversation
        title: New title for the conversation
        user_id: Authenticated user's ID (from JWT)
        session: Database session

    Returns:
        Updated conversation details

    Raises:
        HTTPException 404: If conversation not found or not owned by user
    """
    conv_service = ConversationService(session, user_id)

    conversation = conv_service.update_conversation_title(conversation_id, title)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found"
        )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )
