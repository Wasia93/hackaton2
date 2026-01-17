"""
MCP Tool: complete_task
Task: T-011 - Toggle task completion status
"""

from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session
from app.services.task_service import TaskService
from app.core.database import engine


class CompleteTaskInput(BaseModel):
    """Input schema for complete_task tool"""
    user_id: str = Field(..., description="The user's ID")
    task_id: int = Field(..., description="The task ID to toggle completion")


class CompleteTaskOutput(BaseModel):
    """Output schema for complete_task tool"""
    success: bool
    id: Optional[int] = None
    title: Optional[str] = None
    completed: Optional[bool] = None
    message: Optional[str] = None
    error: Optional[str] = None


async def handle_complete_task(input_data: dict) -> dict:
    """
    Handler for complete_task tool.
    Toggles a task's completion status.

    Args:
        input_data: Dictionary with user_id and task_id

    Returns:
        Dictionary with updated task status or error message
    """
    try:
        validated = CompleteTaskInput(**input_data)

        with Session(engine) as session:
            service = TaskService(session, validated.user_id)
            task = service.toggle_completion(validated.task_id)

            if not task:
                return CompleteTaskOutput(
                    success=False,
                    error=f"Task with ID {validated.task_id} not found"
                ).model_dump()

            status = "completed" if task.completed else "incomplete"
            return CompleteTaskOutput(
                success=True,
                id=task.id,
                title=task.title,
                completed=task.completed,
                message=f"Task '{task.title}' marked as {status}"
            ).model_dump()

    except Exception as e:
        return CompleteTaskOutput(success=False, error=f"Failed to update task: {str(e)}").model_dump()


# Tool definition for OpenAI function calling
complete_task_tool = {
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Toggle a task's completion status. Use this when the user wants to mark a task as done/complete or undo a completion.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID (automatically provided)"
                },
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to mark as complete/incomplete"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
