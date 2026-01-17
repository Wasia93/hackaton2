"""
MCP Tools Package - Task Management Tools for AI Chatbot
Phase III: T-006 to T-013
"""

from app.mcp_tools.create_task import create_task_tool, handle_create_task
from app.mcp_tools.list_tasks import list_tasks_tool, handle_list_tasks
from app.mcp_tools.get_task import get_task_tool, handle_get_task
from app.mcp_tools.update_task import update_task_tool, handle_update_task
from app.mcp_tools.complete_task import complete_task_tool, handle_complete_task
from app.mcp_tools.delete_task import delete_task_tool, handle_delete_task
from app.mcp_tools.search_tasks import search_tasks_tool, handle_search_tasks

# Export all tools and handlers
__all__ = [
    # Tool definitions
    "create_task_tool",
    "list_tasks_tool",
    "get_task_tool",
    "update_task_tool",
    "complete_task_tool",
    "delete_task_tool",
    "search_tasks_tool",
    # Handlers
    "handle_create_task",
    "handle_list_tasks",
    "handle_get_task",
    "handle_update_task",
    "handle_complete_task",
    "handle_delete_task",
    "handle_search_tasks",
]

# List of all tools for registration
ALL_TOOLS = [
    create_task_tool,
    list_tasks_tool,
    get_task_tool,
    update_task_tool,
    complete_task_tool,
    delete_task_tool,
    search_tasks_tool,
]

# Map tool names to handlers
TOOL_HANDLERS = {
    "create_task": handle_create_task,
    "list_tasks": handle_list_tasks,
    "get_task": handle_get_task,
    "update_task": handle_update_task,
    "complete_task": handle_complete_task,
    "delete_task": handle_delete_task,
    "search_tasks": handle_search_tasks,
}
