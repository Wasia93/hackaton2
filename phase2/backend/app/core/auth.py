"""
Authentication middleware for FastAPI
Task: T-011 - Create Authentication Middleware
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token


# HTTP Bearer token authentication scheme
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract and validate JWT token from Authorization header.
    Returns the user_id (subject) from the token.

    This function is used as a FastAPI dependency to protect routes.

    Args:
        credentials: HTTP authorization credentials from request header

    Returns:
        str: User ID extracted from JWT token

    Raises:
        HTTPException: 401 if token is invalid or missing user_id
    """
    token = credentials.credentials

    # Verify and decode token
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from token subject
    user_id: str | None = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload - missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
