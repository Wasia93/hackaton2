"""
Demo authentication endpoints for development
This provides basic login functionality for testing
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request model"""
    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    user_id: str


@router.post("/login", response_model=LoginResponse)
async def demo_login(request: LoginRequest):
    """
    Demo login endpoint for development.
    Accepts any email/password and returns a valid JWT token.

    In production, this would validate credentials against Better Auth.
    """
    # For demo: accept any credentials and create user_id from email
    user_id = request.email.split("@")[0]

    # Generate JWT token
    access_token = create_access_token(data={"sub": user_id})

    return LoginResponse(
        access_token=access_token,
        user_id=user_id
    )


@router.post("/register", response_model=LoginResponse)
async def demo_register(request: LoginRequest):
    """
    Demo register endpoint for development.
    Accepts any email/password and returns a valid JWT token.

    In production, this would create a user via Better Auth.
    """
    # For demo: accept any credentials and create user_id from email
    user_id = request.email.split("@")[0]

    # Generate JWT token
    access_token = create_access_token(data={"sub": user_id})

    return LoginResponse(
        access_token=access_token,
        user_id=user_id
    )
