"""
MCP Tool: delete_task
Task: T-012 - Delete a task
"""

from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session
from app.services.task_service import TaskService
from app.core.database import engine


class DeleteTaskInput(BaseModel):
    """Input schema for delete_task tool"""
    user_id: str = Field(..., description="The user's ID")
    task_id: int = Field(..., description="The task ID to delete")


class DeleteTaskOutput(BaseModel):
    """Output schema for delete_task tool"""
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None


async def handle_delete_task(input_data: dict) -> dict:
    """
    Handler for delete_task tool.
    Deletes a task by ID.

    Args:
        input_data: Dictionary with user_id and task_id

    Returns:
        Dictionary with success status or error message
    """
    try:
        validated = DeleteTaskInput(**input_data)

        with Session(engine) as session:
            service = TaskService(session, validated.user_id)
            deleted = service.delete_task(validated.task_id)

            if not deleted:
                return DeleteTaskOutput(
                    success=False,
                    error=f"Task with ID {validated.task_id} not found"
                ).model_dump()

            return DeleteTaskOutput(
                success=True,
                message=f"Task {validated.task_id} deleted successfully"
            ).model_dump()

    except Exception as e:
        return DeleteTaskOutput(success=False, error=f"Failed to delete task: {str(e)}").model_dump()


# Tool definition for OpenAI function calling
delete_task_tool = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Delete a task permanently. Use this when the user wants to remove a task from their list.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID (automatically provided)"
                },
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
