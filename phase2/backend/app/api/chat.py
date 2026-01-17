"""
Chat API Endpoint
Task: T-022, T-024 - Implement chat API endpoint with error handling

Handles chat messages between users and the AI assistant.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from sqlmodel import Session
from app.core.database import get_session
from app.core.auth import get_current_user_id
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.services.agent_service import process_chat_message
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=4000, description="User's message")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID (optional)")


class ToolCallInfo(BaseModel):
    """Information about a tool call made by the assistant."""
    name: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""
    conversation_id: int
    message_id: int
    content: str
    tool_calls: Optional[List[ToolCallInfo]] = None


class ErrorResponse(BaseModel):
    """Error response body."""
    error: str
    detail: Optional[str] = None


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        200: {"description": "Successful response from AI assistant"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"},
        503: {"model": ErrorResponse, "description": "AI service unavailable"},
    }
)
async def chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI assistant and receive a response.

    The assistant can help with task management:
    - Create new tasks
    - List and search tasks
    - Update task details
    - Mark tasks as complete
    - Delete tasks

    Args:
        request: Chat request with message and optional conversation ID
        user_id: Authenticated user's ID (from JWT)
        session: Database session

    Returns:
        ChatResponse with AI assistant's response

    Raises:
        HTTPException: If message processing fails
    """
    try:
        # Initialize services
        conv_service = ConversationService(session, user_id)
        msg_service = MessageService(session)

        # Get or create conversation
        conversation = conv_service.get_or_create_conversation(request.conversation_id)

        # Auto-generate title from first message if new conversation
        if conversation.title == "New Conversation" and not request.conversation_id:
            # Use first 50 chars of message as title
            title = request.message[:50].strip()
            if len(request.message) > 50:
                title += "..."
            conv_service.update_conversation_title(conversation.id, title)

        # Load conversation history for context
        history = msg_service.get_conversation_history(conversation.id)

        # Save user message
        user_message = msg_service.create_user_message(conversation.id, request.message)

        # Process through AI agent
        try:
            agent_response = await process_chat_message(
                user_id=user_id,
                message_content=request.message,
                conversation_history=history
            )
        except Exception as agent_error:
            logger.error(f"Agent error: {agent_error}")
            # Provide fallback response
            agent_response = {
                "content": "I'm sorry, I'm having trouble processing your request right now. Please try again in a moment.",
                "tool_calls": None
            }

        # Save assistant message
        assistant_message = msg_service.create_assistant_message(
            conversation_id=conversation.id,
            content=agent_response["content"] or "I apologize, I couldn't generate a response.",
            tool_calls=agent_response.get("tool_calls")
        )

        # Update conversation timestamp
        conv_service.update_conversation_timestamp(conversation.id)

        # Format tool calls for response
        tool_calls_info = None
        if agent_response.get("tool_calls"):
            tool_calls_info = [
                ToolCallInfo(
                    name=tc["name"],
                    arguments=tc["arguments"],
                    result=tc["result"]
                )
                for tc in agent_response["tool_calls"]
            ]

        return ChatResponse(
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            content=agent_response["content"] or "",
            tool_calls=tool_calls_info
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/health")
async def chat_health():
    """Check if chat service is available."""
    from app.core.config import settings

    has_gemini_key = bool(settings.GEMINI_API_KEY)
    has_openai_key = bool(settings.OPENAI_API_KEY)

    return {
        "status": "ok" if (has_gemini_key or has_openai_key) else "degraded",
        "gemini_configured": has_gemini_key,
        "openai_configured": has_openai_key,
        "model": settings.GEMINI_MODEL if has_gemini_key else settings.OPENAI_AGENT_MODEL
    }
