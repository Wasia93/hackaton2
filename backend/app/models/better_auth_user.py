"""
Better Auth User model for authentication
Task: T-006 - Create Better Auth User Model
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class BetterAuthUser(SQLModel, table=True):
    """
    BetterAuthUser model mirroring Better Auth schema.
    Handles authentication and password storage.
    Separate from User model for auth isolation.
    """

    __tablename__ = "better_auth_users"

    id: str = Field(primary_key=True)  # UUID from Better Auth
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=200)
    hashed_password: str
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
