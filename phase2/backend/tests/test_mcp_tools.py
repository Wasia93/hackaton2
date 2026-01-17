"""
MCP Tools Test Suite
Task: T-014 - Test all MCP tools

Tests each tool independently:
- Valid inputs return correct outputs
- Invalid inputs raise appropriate errors
- User isolation enforced
- All tools registered correctly
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from sqlmodel import Session, create_engine, SQLModel

# Test database
TEST_DATABASE_URL = "sqlite:///:memory:"


class TestMCPToolsUnit:
    """Unit tests for MCP tools using mocked database."""

    @pytest.fixture(autouse=True)
    def setup_test_db(self):
        """Set up test database and patch the engine."""
        from app.models.task import Task

        # Create test engine
        self.test_engine = create_engine(TEST_DATABASE_URL, echo=False)
        SQLModel.metadata.create_all(self.test_engine)

        # Patch the engine in all tool modules
        with patch('app.mcp_tools.create_task.engine', self.test_engine), \
             patch('app.mcp_tools.list_tasks.engine', self.test_engine), \
             patch('app.mcp_tools.get_task.engine', self.test_engine), \
             patch('app.mcp_tools.update_task.engine', self.test_engine), \
             patch('app.mcp_tools.complete_task.engine', self.test_engine), \
             patch('app.mcp_tools.delete_task.engine', self.test_engine), \
             patch('app.mcp_tools.search_tasks.engine', self.test_engine):
            yield

        SQLModel.metadata.drop_all(self.test_engine)

    def _create_test_task(self, user_id: str, title: str, description: str = "", completed: bool = False):
        """Helper to create a task in test database."""
        from app.models.task import Task

        with Session(self.test_engine) as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=completed
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task.id

    # ==================== create_task tests ====================

    @pytest.mark.asyncio
    async def test_create_task_success(self):
        """Test creating a task with valid input."""
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            result = await handle_create_task({
                "user_id": "user-1",
                "title": "Test Task",
                "description": "Test description"
            })

        assert result["success"] is True
        assert result["title"] == "Test Task"
        assert result["description"] == "Test description"
        assert result["completed"] is False
        assert result["id"] is not None

    @pytest.mark.asyncio
    async def test_create_task_empty_title(self):
        """Test creating a task with empty title fails."""
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            result = await handle_create_task({
                "user_id": "user-1",
                "title": ""
            })

        assert result["success"] is False
        assert "Title is required" in result["error"]

    @pytest.mark.asyncio
    async def test_create_task_title_too_long(self):
        """Test creating a task with title > 200 chars fails."""
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            result = await handle_create_task({
                "user_id": "user-1",
                "title": "x" * 201
            })

        assert result["success"] is False
        assert "200 characters" in result["error"]

    # ==================== list_tasks tests ====================

    @pytest.mark.asyncio
    async def test_list_tasks_empty(self):
        """Test listing tasks when user has none."""
        from app.mcp_tools.list_tasks import handle_list_tasks

        with patch('app.mcp_tools.list_tasks.engine', self.test_engine):
            result = await handle_list_tasks({"user_id": "user-1"})

        assert result["success"] is True
        assert result["tasks"] == []
        assert result["count"] == 0

    @pytest.mark.asyncio
    async def test_list_tasks_with_tasks(self):
        """Test listing tasks when user has some."""
        from app.mcp_tools.list_tasks import handle_list_tasks

        # Create tasks first
        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            from app.mcp_tools.create_task import handle_create_task
            await handle_create_task({"user_id": "user-1", "title": "Task 1"})
            await handle_create_task({"user_id": "user-1", "title": "Task 2"})

        with patch('app.mcp_tools.list_tasks.engine', self.test_engine):
            result = await handle_list_tasks({"user_id": "user-1"})

        assert result["success"] is True
        assert result["count"] == 2
        assert len(result["tasks"]) == 2

    @pytest.mark.asyncio
    async def test_list_tasks_user_isolation(self):
        """Test that users can only see their own tasks."""
        from app.mcp_tools.list_tasks import handle_list_tasks
        from app.mcp_tools.create_task import handle_create_task

        # Create tasks for different users
        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            await handle_create_task({"user_id": "user-1", "title": "User 1 Task"})
            await handle_create_task({"user_id": "user-2", "title": "User 2 Task"})

        with patch('app.mcp_tools.list_tasks.engine', self.test_engine):
            result1 = await handle_list_tasks({"user_id": "user-1"})
            result2 = await handle_list_tasks({"user_id": "user-2"})

        assert result1["count"] == 1
        assert result1["tasks"][0]["title"] == "User 1 Task"
        assert result2["count"] == 1
        assert result2["tasks"][0]["title"] == "User 2 Task"

    # ==================== get_task tests ====================

    @pytest.mark.asyncio
    async def test_get_task_success(self):
        """Test getting a task by ID."""
        from app.mcp_tools.get_task import handle_get_task
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            create_result = await handle_create_task({
                "user_id": "user-1",
                "title": "Test Task",
                "description": "Test desc"
            })

        task_id = create_result["id"]

        with patch('app.mcp_tools.get_task.engine', self.test_engine):
            result = await handle_get_task({
                "user_id": "user-1",
                "task_id": task_id
            })

        assert result["success"] is True
        assert result["id"] == task_id
        assert result["title"] == "Test Task"

    @pytest.mark.asyncio
    async def test_get_task_not_found(self):
        """Test getting a non-existent task."""
        from app.mcp_tools.get_task import handle_get_task

        with patch('app.mcp_tools.get_task.engine', self.test_engine):
            result = await handle_get_task({
                "user_id": "user-1",
                "task_id": 9999
            })

        assert result["success"] is False
        assert "not found" in result["error"]

    @pytest.mark.asyncio
    async def test_get_task_wrong_user(self):
        """Test that user can't access another user's task."""
        from app.mcp_tools.get_task import handle_get_task
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            create_result = await handle_create_task({
                "user_id": "user-1",
                "title": "User 1 Task"
            })

        task_id = create_result["id"]

        with patch('app.mcp_tools.get_task.engine', self.test_engine):
            result = await handle_get_task({
                "user_id": "user-2",  # Different user
                "task_id": task_id
            })

        assert result["success"] is False
        assert "not found" in result["error"]

    # ==================== update_task tests ====================

    @pytest.mark.asyncio
    async def test_update_task_title(self):
        """Test updating a task's title."""
        from app.mcp_tools.update_task import handle_update_task
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            create_result = await handle_create_task({
                "user_id": "user-1",
                "title": "Original Title"
            })

        task_id = create_result["id"]

        with patch('app.mcp_tools.update_task.engine', self.test_engine):
            result = await handle_update_task({
                "user_id": "user-1",
                "task_id": task_id,
                "title": "Updated Title"
            })

        assert result["success"] is True
        assert result["title"] == "Updated Title"

    @pytest.mark.asyncio
    async def test_update_task_no_fields(self):
        """Test updating without providing any fields fails."""
        from app.mcp_tools.update_task import handle_update_task
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            create_result = await handle_create_task({
                "user_id": "user-1",
                "title": "Test"
            })

        task_id = create_result["id"]

        with patch('app.mcp_tools.update_task.engine', self.test_engine):
            result = await handle_update_task({
                "user_id": "user-1",
                "task_id": task_id
            })

        assert result["success"] is False
        assert "at least one field" in result["error"]

    # ==================== complete_task tests ====================

    @pytest.mark.asyncio
    async def test_complete_task_toggle(self):
        """Test toggling task completion."""
        from app.mcp_tools.complete_task import handle_complete_task
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            create_result = await handle_create_task({
                "user_id": "user-1",
                "title": "Test Task"
            })

        task_id = create_result["id"]
        assert create_result["completed"] is False

        # Toggle to complete
        with patch('app.mcp_tools.complete_task.engine', self.test_engine):
            result1 = await handle_complete_task({
                "user_id": "user-1",
                "task_id": task_id
            })

        assert result1["success"] is True
        assert result1["completed"] is True

        # Toggle back to incomplete
        with patch('app.mcp_tools.complete_task.engine', self.test_engine):
            result2 = await handle_complete_task({
                "user_id": "user-1",
                "task_id": task_id
            })

        assert result2["success"] is True
        assert result2["completed"] is False

    # ==================== delete_task tests ====================

    @pytest.mark.asyncio
    async def test_delete_task_success(self):
        """Test deleting a task."""
        from app.mcp_tools.delete_task import handle_delete_task
        from app.mcp_tools.create_task import handle_create_task
        from app.mcp_tools.get_task import handle_get_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            create_result = await handle_create_task({
                "user_id": "user-1",
                "title": "To Delete"
            })

        task_id = create_result["id"]

        with patch('app.mcp_tools.delete_task.engine', self.test_engine):
            result = await handle_delete_task({
                "user_id": "user-1",
                "task_id": task_id
            })

        assert result["success"] is True

        # Verify deleted
        with patch('app.mcp_tools.get_task.engine', self.test_engine):
            get_result = await handle_get_task({
                "user_id": "user-1",
                "task_id": task_id
            })

        assert get_result["success"] is False

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        from app.mcp_tools.delete_task import handle_delete_task

        with patch('app.mcp_tools.delete_task.engine', self.test_engine):
            result = await handle_delete_task({
                "user_id": "user-1",
                "task_id": 9999
            })

        assert result["success"] is False
        assert "not found" in result["error"]

    # ==================== search_tasks tests ====================

    @pytest.mark.asyncio
    async def test_search_tasks_by_keyword(self):
        """Test searching tasks by keyword."""
        from app.mcp_tools.search_tasks import handle_search_tasks
        from app.mcp_tools.create_task import handle_create_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            await handle_create_task({
                "user_id": "user-1",
                "title": "Buy groceries",
                "description": "Milk and eggs"
            })
            await handle_create_task({
                "user_id": "user-1",
                "title": "Call mom",
                "description": "Birthday"
            })
            await handle_create_task({
                "user_id": "user-1",
                "title": "Buy milk separately",
                "description": ""
            })

        with patch('app.mcp_tools.search_tasks.engine', self.test_engine):
            result = await handle_search_tasks({
                "user_id": "user-1",
                "keyword": "milk"
            })

        assert result["success"] is True
        assert result["count"] == 2  # "Buy groceries" (desc) and "Buy milk separately" (title)

    @pytest.mark.asyncio
    async def test_search_tasks_empty_keyword(self):
        """Test searching with empty keyword fails."""
        from app.mcp_tools.search_tasks import handle_search_tasks

        with patch('app.mcp_tools.search_tasks.engine', self.test_engine):
            result = await handle_search_tasks({
                "user_id": "user-1",
                "keyword": "   "
            })

        assert result["success"] is False
        assert "empty" in result["error"]

    @pytest.mark.asyncio
    async def test_search_tasks_completed_filter(self):
        """Test searching with completion filter."""
        from app.mcp_tools.search_tasks import handle_search_tasks
        from app.mcp_tools.create_task import handle_create_task
        from app.mcp_tools.complete_task import handle_complete_task

        with patch('app.mcp_tools.create_task.engine', self.test_engine):
            result1 = await handle_create_task({
                "user_id": "user-1",
                "title": "Task one"
            })
            await handle_create_task({
                "user_id": "user-1",
                "title": "Task two"
            })

        # Complete first task
        with patch('app.mcp_tools.complete_task.engine', self.test_engine):
            await handle_complete_task({
                "user_id": "user-1",
                "task_id": result1["id"]
            })

        # Search only completed
        with patch('app.mcp_tools.search_tasks.engine', self.test_engine):
            result = await handle_search_tasks({
                "user_id": "user-1",
                "keyword": "task",
                "completed_only": True
            })

        assert result["success"] is True
        assert result["count"] == 1
        assert result["tasks"][0]["title"] == "Task one"


class TestMCPServer:
    """Tests for MCP server functionality."""

    def test_all_tools_registered(self):
        """Test that all 7 tools are registered."""
        from app.mcp_server import mcp_server

        tools = mcp_server.get_tools()
        assert len(tools) == 7

        expected_names = [
            "create_task", "list_tasks", "get_task",
            "update_task", "complete_task", "delete_task", "search_tasks"
        ]
        tool_names = mcp_server.get_tool_names()

        for name in expected_names:
            assert name in tool_names

    def test_tool_definitions_format(self):
        """Test that tool definitions are in correct OpenAI format."""
        from app.mcp_server import mcp_server

        for tool in mcp_server.get_tools():
            assert "type" in tool
            assert tool["type"] == "function"
            assert "function" in tool
            assert "name" in tool["function"]
            assert "description" in tool["function"]
            assert "parameters" in tool["function"]

    @pytest.mark.asyncio
    async def test_execute_unknown_tool(self):
        """Test executing an unknown tool raises error."""
        from app.mcp_server import mcp_server

        with pytest.raises(ValueError) as exc_info:
            await mcp_server.execute_tool("unknown_tool", {})

        assert "Unknown tool" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
