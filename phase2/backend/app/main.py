"""
FastAPI application entry point
Task: T-014 - Create FastAPI Application Entry Point
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.tasks import router as tasks_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.core.database import create_db_and_tables
from app.core.auth import get_current_user_id


# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Todo API with multi-user support and JWT authentication",
    version="2.0.0",
)


# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(chat_router)
app.include_router(conversations_router)


# Health check endpoint
@app.get("/health", tags=["system"])
async def health_check():
    """
    Health check endpoint to verify API is running.

    Returns:
        dict: Status message
    """
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": "2.0.0"
    }


# Debug endpoint to test authentication
@app.get("/debug/auth", tags=["system"])
async def debug_auth(user_id: str = Depends(get_current_user_id)):
    """Debug endpoint to test authentication"""
    return {
        "authenticated": True,
        "user_id": user_id
    }


# Root endpoint
@app.get("/", tags=["system"])
async def root():
    """
    Root endpoint with API information.

    Returns:
        dict: API welcome message and documentation link
    """
    return {
        "message": "Todo API - Phase II Full-Stack Application",
        "docs": "/docs",
        "health": "/health"
    }
