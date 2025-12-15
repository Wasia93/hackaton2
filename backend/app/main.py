"""
FastAPI application entry point
Task: T-014 - Create FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.tasks import router as tasks_router


# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Todo API with multi-user support and JWT authentication",
    version="2.0.0",
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Include routers
app.include_router(tasks_router)


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
