"""
MCP Server - Task Management Tools for AI Chatbot
Phase III: T-006 - MCP Server Structure

This module provides the MCP (Model Context Protocol) server that exposes
task management tools to the AI agent. The tools wrap the existing TaskService
methods to provide a natural language interface for task operations.
"""

import json
from typing import Any, Dict, List, Optional
from app.mcp_tools import (
    ALL_TOOLS,
    TOOL_HANDLERS,
    handle_create_task,
    handle_list_tasks,
    handle_get_task,
    handle_update_task,
    handle_complete_task,
    handle_delete_task,
    handle_search_tasks,
)


class MCPServer:
    """
    MCP Server for task management.
    Provides tools for AI agents to interact with the task system.
    """

    def __init__(self):
        """Initialize the MCP server with available tools."""
        self.tools = ALL_TOOLS
        self.handlers = TOOL_HANDLERS

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get all available tools in OpenAI function calling format.

        Returns:
            List of tool definitions compatible with OpenAI API
        """
        return self.tools

    def get_tool_names(self) -> List[str]:
        """
        Get list of all tool names.

        Returns:
            List of tool name strings
        """
        return list(self.handlers.keys())

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name with given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments to pass to the tool

        Returns:
            Dictionary with tool execution result

        Raises:
            ValueError: If tool_name is not found
        """
        if tool_name not in self.handlers:
            raise ValueError(f"Unknown tool: {tool_name}. Available tools: {self.get_tool_names()}")

        handler = self.handlers[tool_name]
        return await handler(arguments)

    async def execute_tool_call(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call from OpenAI API response format.

        Args:
            tool_call: Tool call object from OpenAI API with 'function' key

        Returns:
            Dictionary with tool execution result
        """
        function = tool_call.get("function", {})
        tool_name = function.get("name")
        arguments_str = function.get("arguments", "{}")

        try:
            arguments = json.loads(arguments_str) if isinstance(arguments_str, str) else arguments_str
        except json.JSONDecodeError:
            return {"success": False, "error": f"Invalid JSON arguments: {arguments_str}"}

        return await self.execute_tool(tool_name, arguments)


# Global MCP server instance
mcp_server = MCPServer()


def get_mcp_server() -> MCPServer:
    """
    Get the global MCP server instance.

    Returns:
        MCPServer instance
    """
    return mcp_server


# Convenience functions for direct tool access
async def call_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Convenience function to call a tool directly.

    Args:
        tool_name: Name of the tool to call
        **kwargs: Tool arguments

    Returns:
        Tool execution result
    """
    return await mcp_server.execute_tool(tool_name, kwargs)


# System prompt for AI agent describing available tools
AGENT_SYSTEM_PROMPT = """You are a helpful assistant that manages todo tasks for users.

You have access to the following tools for task management:

1. **create_task**: Create a new task
   - Required: title (max 200 chars)
   - Optional: description

2. **list_tasks**: Get all tasks for the user
   - Shows all tasks with their status

3. **get_task**: Get details of a specific task
   - Required: task_id

4. **update_task**: Update a task's title or description
   - Required: task_id
   - Optional: title, description (at least one required)

5. **complete_task**: Toggle task completion status
   - Required: task_id
   - Marks incomplete tasks as complete, and vice versa

6. **delete_task**: Permanently delete a task
   - Required: task_id

7. **search_tasks**: Search tasks by keyword
   - Required: keyword
   - Optional: completed_only (true/false)

When users ask about their tasks or want to manage them, use these tools appropriately.
Always confirm actions with the user and provide clear feedback about what was done.

Important notes:
- The user_id is automatically provided to all tools - you don't need to ask for it.
- Task IDs are integers that uniquely identify each task.
- When listing tasks, show relevant information like title, status, and ID.
- Be helpful and proactive in suggesting task management actions.
"""
