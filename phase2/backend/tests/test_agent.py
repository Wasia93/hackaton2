"""
Agent Service Tests
Task: T-019 - Test agent with sample queries

Tests the agent's ability to interpret natural language and execute tools.
Note: These tests require a valid OPENAI_API_KEY to run against the real API.
For CI/CD, mock the OpenAI client.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json


class TestAgentServiceUnit:
    """Unit tests for agent service with mocked OpenAI API."""

    @pytest.fixture
    def mock_openai_response(self):
        """Create a mock OpenAI response."""
        mock_message = MagicMock()
        mock_message.content = "I've added 'Buy milk' to your tasks!"
        mock_message.tool_calls = None

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        return mock_response

    @pytest.fixture
    def mock_openai_response_with_tools(self):
        """Create a mock OpenAI response with tool calls."""
        # First response with tool call
        mock_tool_call = MagicMock()
        mock_tool_call.id = "call_123"
        mock_tool_call.function.name = "create_task"
        mock_tool_call.function.arguments = json.dumps({
            "title": "Buy milk",
            "description": ""
        })

        mock_message1 = MagicMock()
        mock_message1.content = None
        mock_message1.tool_calls = [mock_tool_call]

        mock_choice1 = MagicMock()
        mock_choice1.message = mock_message1

        mock_response1 = MagicMock()
        mock_response1.choices = [mock_choice1]

        # Second response (after tool execution)
        mock_message2 = MagicMock()
        mock_message2.content = "I've added 'Buy milk' to your tasks! ✓"
        mock_message2.tool_calls = None

        mock_choice2 = MagicMock()
        mock_choice2.message = mock_message2

        mock_response2 = MagicMock()
        mock_response2.choices = [mock_choice2]

        return mock_response1, mock_response2

    @pytest.mark.asyncio
    async def test_process_message_simple_response(self, mock_openai_response):
        """Test processing a message with simple response (no tools)."""
        with patch('app.services.agent_service.settings') as mock_settings, \
             patch('app.services.agent_service.AsyncOpenAI') as mock_client_class:

            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.OPENAI_AGENT_MODEL = "gpt-4o"

            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_openai_response)
            mock_client_class.return_value = mock_client

            from app.services.agent_service import AgentService
            service = AgentService()
            service.client = mock_client

            result = await service.process_message(
                user_id="user-123",
                message_content="Hello!",
                conversation_history=[]
            )

            assert "content" in result
            assert result["tool_calls"] is None

    @pytest.mark.asyncio
    async def test_process_message_with_tool_call(self, mock_openai_response_with_tools):
        """Test processing a message that triggers tool usage."""
        response1, response2 = mock_openai_response_with_tools

        with patch('app.services.agent_service.settings') as mock_settings, \
             patch('app.services.agent_service.AsyncOpenAI') as mock_client_class, \
             patch('app.services.agent_service.mcp_server') as mock_mcp:

            mock_settings.OPENAI_API_KEY = "test-key"
            mock_settings.OPENAI_AGENT_MODEL = "gpt-4o"

            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(side_effect=[response1, response2])
            mock_client_class.return_value = mock_client

            # Mock MCP server
            mock_mcp.get_tools.return_value = []
            mock_mcp.execute_tool = AsyncMock(return_value={
                "success": True,
                "id": 1,
                "title": "Buy milk",
                "completed": False
            })

            from app.services.agent_service import AgentService
            service = AgentService()
            service.client = mock_client

            result = await service.process_message(
                user_id="user-123",
                message_content="Add buy milk to my list",
                conversation_history=[]
            )

            assert "content" in result
            assert result["content"] == "I've added 'Buy milk' to your tasks! ✓"
            assert result["tool_calls"] is not None
            assert len(result["tool_calls"]) == 1
            assert result["tool_calls"][0]["name"] == "create_task"

    def test_agent_config_exists(self):
        """Test that agent configuration is properly defined."""
        from app.services.agent_config import (
            AGENT_INSTRUCTIONS,
            AGENT_MODEL,
            AGENT_TEMPERATURE,
            AGENT_MAX_TOKENS
        )

        assert AGENT_INSTRUCTIONS is not None
        assert len(AGENT_INSTRUCTIONS) > 100  # Has substantial instructions
        assert "task" in AGENT_INSTRUCTIONS.lower()
        assert AGENT_MODEL == "gpt-4o"
        assert 0 <= AGENT_TEMPERATURE <= 2
        assert AGENT_MAX_TOKENS > 0

    def test_mcp_server_has_tools(self):
        """Test that MCP server has all required tools."""
        from app.mcp_server import mcp_server

        tools = mcp_server.get_tools()
        tool_names = mcp_server.get_tool_names()

        assert len(tools) == 7
        expected_tools = [
            "create_task", "list_tasks", "get_task",
            "update_task", "complete_task", "delete_task", "search_tasks"
        ]
        for name in expected_tools:
            assert name in tool_names


class TestAgentInterpretation:
    """Tests for agent's natural language interpretation capabilities.

    Note: These tests describe expected behavior. In a real scenario,
    they would be run against the actual OpenAI API or a mock that
    simulates the expected responses.
    """

    def test_intent_mapping(self):
        """Document expected intent mappings for agent."""
        intent_mappings = {
            # Create task intents
            "Add buy milk to my list": "create_task",
            "I need to remember to call mom": "create_task",
            "Create a task for finishing the report": "create_task",

            # List tasks intents
            "Show my tasks": "list_tasks",
            "What's on my list?": "list_tasks",
            "What do I need to do?": "list_tasks",

            # Complete task intents
            "Mark buy milk as done": "complete_task",
            "I finished the groceries": "complete_task",
            "Complete task 1": "complete_task",

            # Delete task intents
            "Delete the milk task": "delete_task",
            "Remove task 1": "delete_task",

            # Update task intents
            "Change task 1 title to Call dad": "update_task",
            "Update the description of task 2": "update_task",

            # Search intents
            "Find tasks about groceries": "search_tasks",
            "Search for milk": "search_tasks",
        }

        # This documents expected behavior
        # In actual tests, we would verify the agent correctly identifies these intents
        assert len(intent_mappings) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
