# [Task]: T-004
# [From]: specs/phase3-ai-chatbot/spec.md §3.3, plan.md §3

"""
Message model for Phase III AI chatbot.

Represents an individual message in a conversation.
"""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Any


class Message(SQLModel, table=True):
    """
    Individual message in a conversation.

    Messages alternate between 'user' (human) and 'assistant' (AI) roles.
    Tool calls are stored when the assistant uses MCP tools.

    Attributes:
        id: Unique message identifier (auto-incremented)
        conversation_id: ID of the conversation this message belongs to
        role: Message role ('user' or 'assistant')
        content: Message text content
        tool_calls: JSON array of tool invocations (if assistant used tools)
        created_at: When the message was created
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    tool_calls: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
