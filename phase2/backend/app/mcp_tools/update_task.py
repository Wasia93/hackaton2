"""
MCP Tool: update_task
Task: T-010 - Update task title/description
"""

from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session
from app.services.task_service import TaskService
from app.core.database import engine


class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool"""
    user_id: str = Field(..., description="The user's ID")
    task_id: int = Field(..., description="The task ID to update")
    title: Optional[str] = Field(None, description="New task title (optional)")
    description: Optional[str] = Field(None, description="New task description (optional)")


class UpdateTaskOutput(BaseModel):
    """Output schema for update_task tool"""
    success: bool
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    updated_at: Optional[str] = None
    error: Optional[str] = None


async def handle_update_task(input_data: dict) -> dict:
    """
    Handler for update_task tool.
    Updates a task's title and/or description.

    Args:
        input_data: Dictionary with user_id, task_id, and optional title/description

    Returns:
        Dictionary with updated task details or error message
    """
    try:
        validated = UpdateTaskInput(**input_data)

        # Must provide at least one field to update
        if validated.title is None and validated.description is None:
            return UpdateTaskOutput(
                success=False,
                error="Must provide at least one field to update (title or description)"
            ).model_dump()

        with Session(engine) as session:
            service = TaskService(session, validated.user_id)
            task = service.update_task(
                validated.task_id,
                title=validated.title,
                description=validated.description
            )

            if not task:
                return UpdateTaskOutput(
                    success=False,
                    error=f"Task with ID {validated.task_id} not found"
                ).model_dump()

            return UpdateTaskOutput(
                success=True,
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                updated_at=task.updated_at.isoformat()
            ).model_dump()

    except ValueError as e:
        return UpdateTaskOutput(success=False, error=str(e)).model_dump()
    except Exception as e:
        return UpdateTaskOutput(success=False, error=f"Failed to update task: {str(e)}").model_dump()


# Tool definition for OpenAI function calling
update_task_tool = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Update a task's title or description. Use this when the user wants to modify an existing task's content.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID (automatically provided)"
                },
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task (optional, max 200 characters)"
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task (optional)"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
