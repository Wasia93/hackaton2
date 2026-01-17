"""
MCP Tool: list_tasks
Task: T-008 - List all tasks for user
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from sqlmodel import Session
from app.services.task_service import TaskService
from app.core.database import engine


class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool"""
    user_id: str = Field(..., description="The user's ID")


class TaskItem(BaseModel):
    """Individual task in list"""
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str


class ListTasksOutput(BaseModel):
    """Output schema for list_tasks tool"""
    success: bool
    tasks: Optional[List[TaskItem]] = None
    count: Optional[int] = None
    error: Optional[str] = None


async def handle_list_tasks(input_data: dict) -> dict:
    """
    Handler for list_tasks tool.
    Retrieves all tasks for the specified user.

    Args:
        input_data: Dictionary with user_id

    Returns:
        Dictionary with list of tasks or error message
    """
    try:
        validated = ListTasksInput(**input_data)

        with Session(engine) as session:
            service = TaskService(session, validated.user_id)
            tasks = service.get_all_tasks()

            task_items = [
                TaskItem(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=task.created_at.isoformat(),
                    updated_at=task.updated_at.isoformat()
                )
                for task in tasks
            ]

            return ListTasksOutput(
                success=True,
                tasks=task_items,
                count=len(task_items)
            ).model_dump()

    except Exception as e:
        return ListTasksOutput(success=False, error=f"Failed to list tasks: {str(e)}").model_dump()


# Tool definition for OpenAI function calling
list_tasks_tool = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "Get all tasks for the user. Use this to show the user their todo list or when they ask what tasks they have.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID (automatically provided)"
                }
            },
            "required": ["user_id"]
        }
    }
}
