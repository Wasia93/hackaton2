"""
MCP Tool: create_task
Task: T-007 - Create new task for user
"""

from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session
from app.services.task_service import TaskService
from app.core.database import engine


class CreateTaskInput(BaseModel):
    """Input schema for create_task tool"""
    user_id: str = Field(..., description="The user's ID")
    title: str = Field(..., description="Task title (required, max 200 chars)")
    description: str = Field(default="", description="Task description (optional)")


class CreateTaskOutput(BaseModel):
    """Output schema for create_task tool"""
    success: bool
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    created_at: Optional[str] = None
    error: Optional[str] = None


async def handle_create_task(input_data: dict) -> dict:
    """
    Handler for create_task tool.
    Creates a new task for the specified user.

    Args:
        input_data: Dictionary with user_id, title, and optional description

    Returns:
        Dictionary with task details or error message
    """
    try:
        validated = CreateTaskInput(**input_data)

        with Session(engine) as session:
            service = TaskService(session, validated.user_id)
            task = service.create_task(validated.title, validated.description)

            return CreateTaskOutput(
                success=True,
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at.isoformat()
            ).model_dump()

    except ValueError as e:
        return CreateTaskOutput(success=False, error=str(e)).model_dump()
    except Exception as e:
        return CreateTaskOutput(success=False, error=f"Failed to create task: {str(e)}").model_dump()


# Tool definition for OpenAI function calling
create_task_tool = {
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Create a new task for the user. Use this when the user wants to add a new todo item.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID (automatically provided)"
                },
                "title": {
                    "type": "string",
                    "description": "The task title (required, max 200 characters)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional task description with more details"
                }
            },
            "required": ["user_id", "title"]
        }
    }
}
