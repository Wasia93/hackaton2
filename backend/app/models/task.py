"""
Task model for todo items
Task: T-007 - Create Task SQLModel
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task model representing todo items.
    Each task belongs to a specific user (identified by Better Auth UUID).
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)  # Better Auth UUID
    title: str = Field(max_length=200)
    description: str = Field(default="")
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
