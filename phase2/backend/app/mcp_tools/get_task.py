"""
MCP Tool: get_task
Task: T-009 - Get specific task by ID
"""

from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session
from app.services.task_service import TaskService
from app.core.database import engine


class GetTaskInput(BaseModel):
    """Input schema for get_task tool"""
    user_id: str = Field(..., description="The user's ID")
    task_id: int = Field(..., description="The task ID to retrieve")


class GetTaskOutput(BaseModel):
    """Output schema for get_task tool"""
    success: bool
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    error: Optional[str] = None


async def handle_get_task(input_data: dict) -> dict:
    """
    Handler for get_task tool.
    Retrieves a specific task by ID for the user.

    Args:
        input_data: Dictionary with user_id and task_id

    Returns:
        Dictionary with task details or error message
    """
    try:
        validated = GetTaskInput(**input_data)

        with Session(engine) as session:
            service = TaskService(session, validated.user_id)
            task = service.get_task_by_id(validated.task_id)

            if not task:
                return GetTaskOutput(
                    success=False,
                    error=f"Task with ID {validated.task_id} not found"
                ).model_dump()

            return GetTaskOutput(
                success=True,
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at.isoformat(),
                updated_at=task.updated_at.isoformat()
            ).model_dump()

    except Exception as e:
        return GetTaskOutput(success=False, error=f"Failed to get task: {str(e)}").model_dump()


# Tool definition for OpenAI function calling
get_task_tool = {
    "type": "function",
    "function": {
        "name": "get_task",
        "description": "Get details of a specific task by its ID. Use this when the user wants to see details of a particular task.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID (automatically provided)"
                },
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to retrieve"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
