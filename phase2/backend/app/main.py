"""
FastAPI application entry point
Task: T-014 - Create FastAPI Application Entry Point
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from app.core.config import settings
from app.api.tasks import router as tasks_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.core.database import create_db_and_tables, get_session
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


# Health check endpoint for Kubernetes probes
# [Task]: T-007
# [From]: specs/phase4-kubernetes/spec.md FR-4, specs/phase4-kubernetes/plan.md Section 6.1
@app.get("/health", tags=["system"])
async def health_check(session: Session = Depends(get_session)):
    """
    Health check endpoint for Kubernetes liveness/readiness probes.

    Checks:
    - Database connectivity

    Returns:
        dict: Health status with component checks
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from sqlmodel import text

    checks = {}
    status = "healthy"

    # Check database connection
    try:
        session.exec(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"failed: {str(e)}"
        status = "unhealthy"

    response = {
        "status": status,
        "service": settings.PROJECT_NAME,
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": checks
    }

    if status == "unhealthy":
        return JSONResponse(content=response, status_code=503)
    return response


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
