"""
Task API endpoints
Task: T-013 - Create Task API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.core.auth import get_current_user_id
from app.services.task_service import TaskService
from app.models.task import Task
from pydantic import BaseModel
from typing import Optional


# Router for task endpoints
router = APIRouter(prefix="/tasks", tags=["tasks"])


# Request/Response Models
class CreateTaskRequest(BaseModel):
    """Request model for creating a task"""
    title: str
    description: str = ""


class UpdateTaskRequest(BaseModel):
    """Request model for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None


# API Endpoints

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Create a new task.

    Requires authentication. Task will be associated with the authenticated user.
    """
    try:
        service = TaskService(session, user_id)
        return service.create_task(request.title, request.description)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=list[Task])
async def get_all_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get all tasks for the authenticated user.

    Returns empty list if user has no tasks.
    """
    service = TaskService(session, user_id)
    return service.get_all_tasks()


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific task by ID.

    Returns 404 if task not found or doesn't belong to authenticated user.
    """
    service = TaskService(session, user_id)
    task = service.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Update a task's title and/or description.

    Returns 404 if task not found or doesn't belong to authenticated user.
    """
    try:
        service = TaskService(session, user_id)
        task = service.update_task(task_id, request.title, request.description)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Delete a task by ID.

    Returns 404 if task not found or doesn't belong to authenticated user.
    Returns 204 No Content on successful deletion.
    """
    service = TaskService(session, user_id)

    if not service.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch("/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Toggle a task's completion status (complete ↔ incomplete).

    Returns 404 if task not found or doesn't belong to authenticated user.
    """
    service = TaskService(session, user_id)
    task = service.toggle_completion(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task
