"""
MCP Tool: search_tasks
Task: T-013 - Search tasks by keyword
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from sqlmodel import Session, select
from app.models.task import Task
from app.core.database import engine


class SearchTasksInput(BaseModel):
    """Input schema for search_tasks tool"""
    user_id: str = Field(..., description="The user's ID")
    keyword: str = Field(..., description="Keyword to search for in task titles and descriptions")
    completed_only: Optional[bool] = Field(None, description="Filter by completion status (True/False/None for all)")


class SearchTaskItem(BaseModel):
    """Individual task in search results"""
    id: int
    title: str
    description: str
    completed: bool
    created_at: str


class SearchTasksOutput(BaseModel):
    """Output schema for search_tasks tool"""
    success: bool
    tasks: Optional[List[SearchTaskItem]] = None
    count: Optional[int] = None
    keyword: Optional[str] = None
    error: Optional[str] = None


async def handle_search_tasks(input_data: dict) -> dict:
    """
    Handler for search_tasks tool.
    Searches tasks by keyword in title or description.

    Args:
        input_data: Dictionary with user_id, keyword, and optional completed_only filter

    Returns:
        Dictionary with matching tasks or error message
    """
    try:
        validated = SearchTasksInput(**input_data)
        keyword = validated.keyword.strip().lower()

        if not keyword:
            return SearchTasksOutput(
                success=False,
                error="Keyword cannot be empty"
            ).model_dump()

        with Session(engine) as session:
            # Base query for user's tasks
            statement = select(Task).where(Task.user_id == validated.user_id)

            # Apply completion filter if specified
            if validated.completed_only is not None:
                statement = statement.where(Task.completed == validated.completed_only)

            all_tasks = session.exec(statement).all()

            # Filter by keyword (case-insensitive search in title and description)
            matching_tasks = [
                task for task in all_tasks
                if keyword in task.title.lower() or keyword in task.description.lower()
            ]

            task_items = [
                SearchTaskItem(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=task.created_at.isoformat()
                )
                for task in matching_tasks
            ]

            return SearchTasksOutput(
                success=True,
                tasks=task_items,
                count=len(task_items),
                keyword=validated.keyword
            ).model_dump()

    except Exception as e:
        return SearchTasksOutput(success=False, error=f"Failed to search tasks: {str(e)}").model_dump()


# Tool definition for OpenAI function calling
search_tasks_tool = {
    "type": "function",
    "function": {
        "name": "search_tasks",
        "description": "Search tasks by keyword in title or description. Use this when the user wants to find specific tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID (automatically provided)"
                },
                "keyword": {
                    "type": "string",
                    "description": "The keyword to search for in task titles and descriptions"
                },
                "completed_only": {
                    "type": "boolean",
                    "description": "If true, only return completed tasks. If false, only incomplete. If not provided, return all."
                }
            },
            "required": ["user_id", "keyword"]
        }
    }
}
