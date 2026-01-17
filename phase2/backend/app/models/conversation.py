# [Task]: T-003
# [From]: specs/phase3-ai-chatbot/spec.md §3.3, plan.md §3

"""
Conversation model for Phase III AI chatbot.

Represents a conversation between a user and the AI assistant.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Conversation(SQLModel, table=True):
    """
    Conversation between user and AI assistant.

    A conversation contains multiple messages and belongs to a single user.
    Used to persist chat history for context retention across sessions.

    Attributes:
        id: Unique conversation identifier (auto-incremented)
        user_id: ID of the user who owns this conversation
        title: Conversation title (auto-generated from first message)
        created_at: When the conversation was started
        updated_at: Last time a message was added to this conversation
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)
    title: str = Field(default="New Conversation", max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
