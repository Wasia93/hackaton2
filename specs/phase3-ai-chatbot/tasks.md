# Phase III: AI Chatbot with MCP - Task Breakdown

**Project**: Evolution of Todo - Phase III
**Generated**: 2026-01-13
**Total Tasks**: 30 atomic work units

---

## Task Summary

| Task ID | Description | Status | Dependencies | Est. Time |
|---------|-------------|--------|--------------|-----------|
| **Phase A: Database & Models** |||||
| T-001 | Create database migration for conversations table | ⬜ | Phase II DB | 30 min |
| T-002 | Create database migration for messages table | ⬜ | T-001 | 30 min |
| T-003 | Create Conversation SQLModel | ⬜ | T-001 | 20 min |
| T-004 | Create Message SQLModel | ⬜ | T-002 | 20 min |
| **Phase B: MCP Server** |||||
| T-005 | Install MCP SDK and dependencies | ⬜ | None | 15 min |
| T-006 | Create MCP server structure | ⬜ | T-005 | 30 min |
| T-007 | Implement create_task MCP tool | ⬜ | T-006 | 45 min |
| T-008 | Implement list_tasks MCP tool | ⬜ | T-006 | 45 min |
| T-009 | Implement get_task MCP tool | ⬜ | T-006 | 30 min |
| T-010 | Implement update_task MCP tool | ⬜ | T-006 | 45 min |
| T-011 | Implement complete_task MCP tool | ⬜ | T-006 | 30 min |
| T-012 | Implement delete_task MCP tool | ⬜ | T-006 | 30 min |
| T-013 | Implement search_tasks MCP tool | ⬜ | T-006 | 45 min |
| T-014 | Test all MCP tools independently | ⬜ | T-007-013 | 1 hour |
| **Phase C: OpenAI Agent** |||||
| T-015 | Install OpenAI SDK and Agents SDK | ⬜ | None | 15 min |
| T-016 | Create AI agent configuration | ⬜ | T-015 | 30 min |
| T-017 | Integrate MCP tools with agent | ⬜ | T-014, T-016 | 45 min |
| T-018 | Create agent service layer | ⬜ | T-017 | 1 hour |
| T-019 | Test agent with sample queries | ⬜ | T-018 | 1 hour |
| **Phase D: Chat API** |||||
| T-020 | Create conversation service | ⬜ | T-003, T-004 | 1 hour |
| T-021 | Create message service | ⬜ | T-003, T-004 | 45 min |
| T-022 | Implement chat API endpoint | ⬜ | T-020, T-021, T-018 | 1 hour |
| T-023 | Add conversation history loading | ⬜ | T-020 | 30 min |
| T-024 | Add error handling for OpenAI API | ⬜ | T-022 | 45 min |
| T-025 | Test chat endpoint end-to-end | ⬜ | T-022 | 1 hour |
| **Phase E: Frontend** |||||
| T-026 | Install OpenAI ChatKit | ⬜ | Phase II frontend | 15 min |
| T-027 | Create Chatbot component | ⬜ | T-026 | 2 hours |
| T-028 | Integrate chat API client | ⬜ | T-027 | 1 hour |
| T-029 | Add chatbot to dashboard | ⬜ | T-028 | 30 min |
| T-030 | Test complete user flow | ⬜ | T-029 | 1 hour |

**Total Estimated Time**: ~20 hours

---

## Phase A: Database & Models

### T-001: Create Database Migration for Conversations Table

**Priority**: CRITICAL
**Dependencies**: Phase II Database
**Estimated Time**: 30 minutes

**Description**: Create Alembic migration to add conversations table

**Acceptance Criteria**:
- ✅ Migration file created in `backend/alembic/versions/`
- ✅ Conversations table schema matches plan.md
- ✅ Indexes created on user_id and updated_at
- ✅ Foreign key to users table exists
- ✅ Migration runs successfully
- ✅ Migration can be rolled back

**Implementation**:
```bash
cd backend
alembic revision -m "Add conversations table"
```

Edit migration file:
```python
def upgrade():
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('title', sa.String(200), default='New Conversation'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.Index('idx_user_conversations', 'user_id', 'updated_at')
    )

def downgrade():
    op.drop_table('conversations')
```

**Testing**:
```bash
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

---

### T-002: Create Database Migration for Messages Table

**Priority**: CRITICAL
**Dependencies**: T-001
**Estimated Time**: 30 minutes

**Description**: Create Alembic migration to add messages table

**Acceptance Criteria**:
- ✅ Migration file created
- ✅ Messages table schema matches plan.md
- ✅ Indexes created on conversation_id
- ✅ Foreign key to conversations table exists
- ✅ JSONB column for tool_calls exists
- ✅ Migration runs successfully
- ✅ Migration can be rolled back

**Implementation**:
```python
def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.Index('idx_conversation_messages', 'conversation_id', 'created_at')
    )

def downgrade():
    op.drop_table('messages')
```

---

### T-003: Create Conversation SQLModel

**Priority**: CRITICAL
**Dependencies**: T-001
**Estimated Time**: 20 minutes
**File**: `backend/app/models/conversation.py`

**Acceptance Criteria**:
- ✅ Conversation model defined with all fields
- ✅ Type hints for all fields
- ✅ Foreign key to user defined
- ✅ Default values set correctly
- ✅ Can be imported without errors

**Implementation**:
```python
# [Task]: T-003
# [From]: specs/phase3-ai-chatbot/spec.md §3.3, plan.md §3

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Conversation(SQLModel, table=True):
    """Conversation between user and AI assistant."""
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)
    title: str = Field(default="New Conversation", max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### T-004: Create Message SQLModel

**Priority**: CRITICAL
**Dependencies**: T-002
**Estimated Time**: 20 minutes
**File**: `backend/app/models/message.py`

**Acceptance Criteria**:
- ✅ Message model defined with all fields
- ✅ Type hints for all fields
- ✅ Foreign key to conversation defined
- ✅ JSONB field for tool_calls
- ✅ Can be imported without errors

**Implementation**:
```python
# [Task]: T-004
# [From]: specs/phase3-ai-chatbot/spec.md §3.3, plan.md §3

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Any

class Message(SQLModel, table=True):
    """Individual message in a conversation."""
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    tool_calls: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Phase B: MCP Server

### T-005: Install MCP SDK and Dependencies

**Priority**: CRITICAL
**Dependencies**: None
**Estimated Time**: 15 minutes

**Acceptance Criteria**:
- ✅ MCP SDK installed in backend
- ✅ Requirements.txt updated
- ✅ Dependencies resolve without conflicts
- ✅ Can import mcp module

**Implementation**:
```bash
cd backend
pip install mcp>=0.1.0
pip freeze | grep mcp >> requirements.txt
```

Test import:
```python
python -c "from mcp import Server; print('MCP SDK installed')"
```

---

### T-006: Create MCP Server Structure

**Priority**: CRITICAL
**Dependencies**: T-005
**Estimated Time**: 30 minutes
**Files**: `backend/app/mcp_server.py`, `backend/app/mcp_tools/__init__.py`

**Acceptance Criteria**:
- ✅ MCP server instance created
- ✅ Server can start without errors
- ✅ Tools directory structure exists
- ✅ Helper functions for tool registration

**Implementation**:
```python
# backend/app/mcp_server.py
# [Task]: T-006

from mcp import Server

# Create MCP server instance
mcp_server = Server("todo-mcp-server")

def get_mcp_tools():
    """Return list of registered MCP tools for OpenAI agent"""
    return mcp_server.list_tools()

def register_tool(tool):
    """Helper to register a tool with the server"""
    mcp_server.add_tool(tool)
```

```python
# backend/app/mcp_tools/__init__.py
# Tool modules will be imported here
```

---

### T-007: Implement create_task MCP Tool

**Priority**: CRITICAL
**Dependencies**: T-006
**Estimated Time**: 45 minutes
**File**: `backend/app/mcp_tools/create_task.py`

**Acceptance Criteria**:
- ✅ Tool definition with schema
- ✅ Handler function implemented
- ✅ Calls Phase II TaskService
- ✅ Validates user_id
- ✅ Returns typed output
- ✅ Error handling included

**Implementation**:
```python
# [Task]: T-007
# [From]: specs/phase3-ai-chatbot/spec.md §3.1, plan.md §4

from mcp import Tool
from pydantic import BaseModel, Field
from app.services.task_service import TaskService
from app.core.database import get_session

class CreateTaskInput(BaseModel):
    user_id: str = Field(description="The authenticated user's ID")
    title: str = Field(description="Task title (max 200 chars)")
    description: str = Field(default="", description="Optional task description")

class CreateTaskOutput(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str

async def handle_create_task(input: CreateTaskInput) -> CreateTaskOutput:
    """Create a new task for the user"""
    with get_session() as session:
        service = TaskService(session, input.user_id)
        task = service.create_task(input.title, input.description)

        return CreateTaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat()
        )

create_task_tool = Tool(
    name="create_task",
    description="Create a new task for the user. Use this when the user wants to add something to their todo list.",
    input_schema=CreateTaskInput.schema(),
    handler=handle_create_task
)
```

---

### T-008: Implement list_tasks MCP Tool

**Priority**: CRITICAL
**Dependencies**: T-006
**Estimated Time**: 45 minutes
**File**: `backend/app/mcp_tools/list_tasks.py`

**Acceptance Criteria**:
- ✅ Tool definition with optional filter
- ✅ Handler returns all tasks for user
- ✅ Supports filter: all, completed, pending
- ✅ Returns task list with all fields

**Implementation**:
```python
# [Task]: T-008

from typing import Literal, List
from pydantic import BaseModel, Field

class ListTasksInput(BaseModel):
    user_id: str
    filter: Literal["all", "completed", "pending"] = Field(
        default="all",
        description="Filter tasks by completion status"
    )

class TaskOutput(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str

class ListTasksOutput(BaseModel):
    tasks: List[TaskOutput]
    total: int

async def handle_list_tasks(input: ListTasksInput) -> ListTasksOutput:
    """List all tasks for the user with optional filter"""
    with get_session() as session:
        service = TaskService(session, input.user_id)
        all_tasks = service.get_all_tasks()

        # Apply filter
        if input.filter == "completed":
            filtered = [t for t in all_tasks if t.completed]
        elif input.filter == "pending":
            filtered = [t for t in all_tasks if not t.completed]
        else:
            filtered = all_tasks

        return ListTasksOutput(
            tasks=[
                TaskOutput(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    completed=t.completed,
                    created_at=t.created_at.isoformat()
                )
                for t in filtered
            ],
            total=len(filtered)
        )

list_tasks_tool = Tool(
    name="list_tasks",
    description="Get all tasks for the user. Can filter by completion status (all, completed, or pending).",
    input_schema=ListTasksInput.schema(),
    handler=handle_list_tasks
)
```

---

### T-009: Implement get_task MCP Tool

**Priority**: HIGH
**Dependencies**: T-006
**Estimated Time**: 30 minutes
**File**: `backend/app/mcp_tools/get_task.py`

**Acceptance Criteria**:
- ✅ Tool gets specific task by ID
- ✅ Validates task belongs to user
- ✅ Returns task details or error

**Implementation**:
```python
# [Task]: T-009

class GetTaskInput(BaseModel):
    user_id: str
    task_id: int = Field(description="The ID of the task to retrieve")

async def handle_get_task(input: GetTaskInput) -> TaskOutput:
    """Get a specific task by ID"""
    with get_session() as session:
        service = TaskService(session, input.user_id)
        task = service.get_task_by_id(input.task_id)

        if not task:
            raise ValueError(f"Task {input.task_id} not found")

        return TaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat()
        )

get_task_tool = Tool(
    name="get_task",
    description="Get a specific task by its ID",
    input_schema=GetTaskInput.schema(),
    handler=handle_get_task
)
```

---

### T-010: Implement update_task MCP Tool

**Priority**: CRITICAL
**Dependencies**: T-006
**Estimated Time**: 45 minutes
**File**: `backend/app/mcp_tools/update_task.py`

**Acceptance Criteria**:
- ✅ Tool updates task title and/or description
- ✅ Validates task belongs to user
- ✅ Returns updated task

**Implementation**:
```python
# [Task]: T-010

from typing import Optional

class UpdateTaskInput(BaseModel):
    user_id: str
    task_id: int
    title: Optional[str] = Field(None, description="New title (optional)")
    description: Optional[str] = Field(None, description="New description (optional)")

async def handle_update_task(input: UpdateTaskInput) -> TaskOutput:
    """Update task title and/or description"""
    with get_session() as session:
        service = TaskService(session, input.user_id)
        task = service.update_task(
            input.task_id,
            title=input.title,
            description=input.description
        )

        if not task:
            raise ValueError(f"Task {input.task_id} not found")

        return TaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat()
        )

update_task_tool = Tool(
    name="update_task",
    description="Update a task's title and/or description",
    input_schema=UpdateTaskInput.schema(),
    handler=handle_update_task
)
```

---

### T-011: Implement complete_task MCP Tool

**Priority**: CRITICAL
**Dependencies**: T-006
**Estimated Time**: 30 minutes
**File**: `backend/app/mcp_tools/complete_task.py`

**Acceptance Criteria**:
- ✅ Tool toggles task completion status
- ✅ Validates task belongs to user
- ✅ Returns updated task

**Implementation**:
```python
# [Task]: T-011

class CompleteTaskInput(BaseModel):
    user_id: str
    task_id: int

async def handle_complete_task(input: CompleteTaskInput) -> TaskOutput:
    """Toggle task completion status"""
    with get_session() as session:
        service = TaskService(session, input.user_id)
        task = service.toggle_complete(input.task_id)

        if not task:
            raise ValueError(f"Task {input.task_id} not found")

        return TaskOutput(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat()
        )

complete_task_tool = Tool(
    name="complete_task",
    description="Mark a task as complete or incomplete (toggles status)",
    input_schema=CompleteTaskInput.schema(),
    handler=handle_complete_task
)
```

---

### T-012: Implement delete_task MCP Tool

**Priority**: CRITICAL
**Dependencies**: T-006
**Estimated Time**: 30 minutes
**File**: `backend/app/mcp_tools/delete_task.py`

**Acceptance Criteria**:
- ✅ Tool deletes task by ID
- ✅ Validates task belongs to user
- ✅ Returns success status

**Implementation**:
```python
# [Task]: T-012

class DeleteTaskInput(BaseModel):
    user_id: str
    task_id: int

class DeleteTaskOutput(BaseModel):
    success: bool
    message: str

async def handle_delete_task(input: DeleteTaskInput) -> DeleteTaskOutput:
    """Delete a task permanently"""
    with get_session() as session:
        service = TaskService(session, input.user_id)
        success = service.delete_task(input.task_id)

        if success:
            return DeleteTaskOutput(
                success=True,
                message=f"Task {input.task_id} deleted successfully"
            )
        else:
            return DeleteTaskOutput(
                success=False,
                message=f"Task {input.task_id} not found"
            )

delete_task_tool = Tool(
    name="delete_task",
    description="Delete a task permanently. Use with caution.",
    input_schema=DeleteTaskInput.schema(),
    handler=handle_delete_task
)
```

---

### T-013: Implement search_tasks MCP Tool

**Priority**: MEDIUM
**Dependencies**: T-006
**Estimated Time**: 45 minutes
**File**: `backend/app/mcp_tools/search_tasks.py`

**Acceptance Criteria**:
- ✅ Tool searches tasks by keyword
- ✅ Searches in title and description
- ✅ Case-insensitive search
- ✅ Returns matching tasks

**Implementation**:
```python
# [Task]: T-013

class SearchTasksInput(BaseModel):
    user_id: str
    query: str = Field(description="Search keyword or phrase")

async def handle_search_tasks(input: SearchTasksInput) -> ListTasksOutput:
    """Search tasks by keyword in title or description"""
    with get_session() as session:
        service = TaskService(session, input.user_id)
        all_tasks = service.get_all_tasks()

        # Case-insensitive search
        query_lower = input.query.lower()
        matching = [
            t for t in all_tasks
            if query_lower in t.title.lower() or query_lower in t.description.lower()
        ]

        return ListTasksOutput(
            tasks=[
                TaskOutput(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    completed=t.completed,
                    created_at=t.created_at.isoformat()
                )
                for t in matching
            ],
            total=len(matching)
        )

search_tasks_tool = Tool(
    name="search_tasks",
    description="Search for tasks containing a specific keyword or phrase",
    input_schema=SearchTasksInput.schema(),
    handler=handle_search_tasks
)
```

---

### T-014: Test All MCP Tools Independently

**Priority**: CRITICAL
**Dependencies**: T-007 through T-013
**Estimated Time**: 1 hour
**File**: `backend/tests/test_mcp_tools.py`

**Acceptance Criteria**:
- ✅ All 7 tools tested
- ✅ Success cases verified
- ✅ Error cases handled
- ✅ User isolation verified
- ✅ All tests pass

**Implementation**:
```python
# [Task]: T-014

import pytest
from app.mcp_tools import (
    create_task_tool,
    list_tasks_tool,
    get_task_tool,
    update_task_tool,
    complete_task_tool,
    delete_task_tool,
    search_tasks_tool
)

@pytest.mark.asyncio
async def test_create_task():
    result = await create_task_tool.handler({
        "user_id": "test-user",
        "title": "Test Task",
        "description": "Test description"
    })
    assert result.title == "Test Task"
    assert result.completed == False

@pytest.mark.asyncio
async def test_list_tasks():
    result = await list_tasks_tool.handler({
        "user_id": "test-user",
        "filter": "all"
    })
    assert isinstance(result.tasks, list)

# ... tests for other tools ...
```

---

## Phase C: OpenAI Agent

### T-015: Install OpenAI SDK and Agents SDK

**Priority**: CRITICAL
**Dependencies**: None
**Estimated Time**: 15 minutes

**Acceptance Criteria**:
- ✅ OpenAI SDK installed (>=1.0.0)
- ✅ OpenAI Agents SDK installed (beta)
- ✅ Requirements.txt updated
- ✅ Can import openai.agents

**Implementation**:
```bash
cd backend
pip install openai>=1.0.0
pip install openai-agents-sdk  # Beta version
pip freeze | grep openai >> requirements.txt
```

---

### T-016: Create AI Agent Configuration

**Priority**: CRITICAL
**Dependencies**: T-015
**Estimated Time**: 30 minutes
**File**: `backend/app/config/agent_config.py`

**Acceptance Criteria**:
- ✅ Agent instructions defined
- ✅ Model configuration set
- ✅ System prompt comprehensive
- ✅ Configuration follows plan.md

**Implementation**:
```python
# [Task]: T-016
# [From]: specs/phase3-ai-chatbot/spec.md §3.2, plan.md §5

AGENT_INSTRUCTIONS = """
You are a friendly and helpful todo list assistant. You help users manage their tasks through natural conversation.

Your capabilities:
- Create new tasks when users describe things they need to do
- Show task lists when users ask what's on their list
- Update task details when users want to modify them
- Mark tasks as complete when users finish them
- Delete tasks when users no longer need them
- Search for specific tasks

Guidelines:
1. Always be encouraging and positive
2. Celebrate when users complete tasks (use emojis like ✓, 🎉)
3. Format task lists clearly with status indicators (✓ complete, ✗ pending)
4. Ask for clarification if the user's intent is ambiguous
5. Confirm actions clearly ("Added 'Buy milk' to your tasks")
6. When listing tasks, show title, status, and creation date
7. If a user refers to "the first task" or "that task", use conversation context
8. Be concise but friendly - keep responses under 3 sentences when possible
9. Use tools to actually perform actions - don't just say you'll do something

Task formatting example:
1. ✓ Buy groceries (completed) - Created Jan 13
2. ✗ Call dentist (pending) - Created Jan 12

Remember: You have real tools to create, update, and delete tasks. Always use them!
"""

AGENT_MODEL = "gpt-4o"  # GPT-4 Optimized
```

---

### T-017: Integrate MCP Tools with Agent

**Priority**: CRITICAL
**Dependencies**: T-014, T-016
**Estimated Time**: 45 minutes
**File**: `backend/app/services/ai_agent.py`

**Acceptance Criteria**:
- ✅ Agent has access to all MCP tools
- ✅ Tool schemas properly formatted
- ✅ Agent can invoke tools
- ✅ Tool responses handled correctly

**Implementation**:
```python
# [Task]: T-017

from openai import OpenAI
from openai.agents import Agent
from app.core.config import settings
from app.mcp_server import get_mcp_tools
from app.config.agent_config import AGENT_INSTRUCTIONS, AGENT_MODEL

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def create_agent():
    """Create and configure the OpenAI agent with MCP tools"""
    mcp_tools = get_mcp_tools()

    agent = Agent(
        name="Todo Assistant",
        instructions=AGENT_INSTRUCTIONS,
        model=AGENT_MODEL,
        tools=mcp_tools,
        client=client
    )

    return agent

# Singleton instance
todo_agent = create_agent()
```

---

### T-018: Create Agent Service Layer

**Priority**: CRITICAL
**Dependencies**: T-017
**Estimated Time**: 1 hour
**File**: `backend/app/services/agent_service.py`

**Acceptance Criteria**:
- ✅ Service processes messages through agent
- ✅ Conversation history passed to agent
- ✅ User context injected into tool calls
- ✅ Agent responses parsed correctly
- ✅ Tool call results captured

**Implementation**:
```python
# [Task]: T-018

from app.services.ai_agent import todo_agent
from typing import List, Dict

async def process_chat_message(
    user_id: str,
    message_content: str,
    conversation_history: List[Dict]
) -> Dict:
    """
    Process a user message through the agent

    Args:
        user_id: Authenticated user ID
        message_content: User's message
        conversation_history: Previous messages for context

    Returns:
        {
            "content": "Agent's response text",
            "tool_calls": [...],  # Tools the agent used
        }
    """

    # Build messages list (history + new message)
    messages = conversation_history + [
        {"role": "user", "content": message_content}
    ]

    # Inject user_id into all tool calls via context
    tool_context = {"user_id": user_id}

    # Run agent
    response = await todo_agent.run(
        messages=messages,
        context=tool_context
    )

    return {
        "content": response.content,
        "tool_calls": response.tool_calls if hasattr(response, 'tool_calls') else None
    }
```

---

### T-019: Test Agent with Sample Queries

**Priority**: CRITICAL
**Dependencies**: T-018
**Estimated Time**: 1 hour
**File**: `backend/tests/test_agent.py`

**Acceptance Criteria**:
- ✅ Agent interprets task creation intents
- ✅ Agent lists tasks correctly
- ✅ Agent handles updates and completions
- ✅ Agent provides friendly responses
- ✅ All test scenarios pass

**Testing Scenarios**:
1. "Add buy milk to my list" → creates task
2. "Show my tasks" → lists tasks
3. "Mark milk as done" → completes task
4. "Delete the milk task" → deletes task
5. "What do I need to do?" → lists tasks

---

## Phase D: Chat API

### T-020: Create Conversation Service

**Priority**: CRITICAL
**Dependencies**: T-003, T-004
**Estimated Time**: 1 hour
**File**: `backend/app/services/conversation_service.py`

**Acceptance Criteria**:
- ✅ Create new conversations
- ✅ Get conversation by ID
- ✅ List user's conversations
- ✅ Load conversation history
- ✅ Data isolation enforced

**Implementation**: See plan.md §6.2

---

### T-021: Create Message Service

**Priority**: CRITICAL
**Dependencies**: T-003, T-004
**Estimated Time**: 45 minutes
**File**: `backend/app/services/message_service.py`

**Acceptance Criteria**:
- ✅ Create user messages
- ✅ Create assistant messages
- ✅ Load message history
- ✅ Store tool call details

---

### T-022: Implement Chat API Endpoint

**Priority**: CRITICAL
**Dependencies**: T-020, T-021, T-018
**Estimated Time**: 1 hour
**File**: `backend/app/api/chat.py`

**Acceptance Criteria**:
- ✅ POST /api/chat endpoint exists
- ✅ Requires JWT authentication
- ✅ Creates conversation if null
- ✅ Saves user message
- ✅ Processes through agent
- ✅ Saves assistant message
- ✅ Returns response

**Implementation**: See plan.md §6.1

---

### T-023: Add Conversation History Loading

**Priority**: HIGH
**Dependencies**: T-020
**Estimated Time**: 30 minutes
**File**: `backend/app/api/conversations.py`

**Acceptance Criteria**:
- ✅ GET /api/conversations endpoint
- ✅ Lists user's conversations
- ✅ GET /api/conversations/{id}/messages
- ✅ Returns conversation messages

---

### T-024: Add Error Handling for OpenAI API

**Priority**: HIGH
**Dependencies**: T-022
**Estimated Time**: 45 minutes

**Acceptance Criteria**:
- ✅ Rate limit errors handled gracefully
- ✅ Timeout errors caught
- ✅ Fallback messages provided
- ✅ Errors logged appropriately

---

### T-025: Test Chat Endpoint End-to-End

**Priority**: CRITICAL
**Dependencies**: T-022
**Estimated Time**: 1 hour
**File**: `backend/tests/test_chat_endpoint.py`

**Acceptance Criteria**:
- ✅ Full flow tested: message → agent → response
- ✅ Conversation persistence verified
- ✅ User isolation verified
- ✅ Error cases handled

---

## Phase E: Frontend

### T-026: Install OpenAI ChatKit

**Priority**: CRITICAL
**Dependencies**: Phase II frontend
**Estimated Time**: 15 minutes

**Acceptance Criteria**:
- ✅ ChatKit package installed
- ✅ Dependencies resolve correctly
- ✅ Can import Chat component

**Implementation**:
```bash
cd frontend
npm install @openai/chatkit
```

---

### T-027: Create Chatbot Component

**Priority**: CRITICAL
**Dependencies**: T-026
**Estimated Time**: 2 hours
**File**: `frontend/components/Chatbot.tsx`

**Acceptance Criteria**:
- ✅ Modal/sidebar chatbot UI
- ✅ Message display
- ✅ Input field
- ✅ Send button
- ✅ Typing indicator
- ✅ Auto-scroll to latest
- ✅ Responsive design

**Implementation**: See plan.md §7.1

---

### T-028: Integrate Chat API Client

**Priority**: CRITICAL
**Dependencies**: T-027
**Estimated Time**: 1 hour

**Acceptance Criteria**:
- ✅ POST /api/chat calls work
- ✅ JWT token included
- ✅ Responses handled correctly
- ✅ Errors displayed to user

---

### T-029: Add Chatbot to Dashboard

**Priority**: CRITICAL
**Dependencies**: T-028
**Estimated Time**: 30 minutes
**File**: `frontend/app/dashboard/page.tsx`

**Acceptance Criteria**:
- ✅ Chat button visible on dashboard
- ✅ Chatbot opens on click
- ✅ Can be closed
- ✅ Doesn't interfere with task list

**Implementation**: See plan.md §7.2

---

### T-030: Test Complete User Flow

**Priority**: CRITICAL
**Dependencies**: T-029
**Estimated Time**: 1 hour

**Testing Scenarios**:
1. Open chatbot from dashboard
2. Create task via chat: "Add buy milk"
3. Verify task appears in web UI
4. List tasks via chat: "Show my tasks"
5. Complete task via chat: "Mark milk as done"
6. Verify completion in web UI
7. Delete task via chat: "Delete milk"
8. Verify deletion in web UI
9. Test multi-turn conversation
10. Test context retention after page refresh

**Acceptance Criteria**:
- ✅ All operations work via chat
- ✅ Changes reflected in web UI immediately
- ✅ Conversation persists across refreshes
- ✅ User cannot see other users' conversations
- ✅ Performance is acceptable (< 5s response time)

---

## Implementation Order

**Week 1**: Backend (Phase A-D)
1. Days 1-2: Database & Models (T-001 to T-004)
2. Days 3-4: MCP Server (T-005 to T-014)
3. Days 5-6: OpenAI Agent (T-015 to T-019)
4. Day 7: Chat API (T-020 to T-025)

**Week 2**: Frontend & Testing (Phase E)
1. Days 1-2: ChatKit Integration (T-026 to T-028)
2. Day 3: Dashboard Integration (T-029)
3. Day 4: End-to-End Testing (T-030)
4. Day 5: Polish & Bug Fixes
5. Days 6-7: Documentation & Deployment

---

## Dependencies Graph

```
T-001 → T-002 → T-003, T-004

T-005 → T-006 → T-007, T-008, T-009, T-010, T-011, T-012, T-013
           ↓
        T-014

T-015 → T-016 → T-017 → T-018 → T-019

T-003, T-004 → T-020, T-021
T-020, T-021, T-018 → T-022 → T-023, T-024 → T-025

T-026 → T-027 → T-028 → T-029 → T-030
```

---

**Task Breakdown Version**: 1.0.0
**Status**: Ready for Implementation
**Total Tasks**: 30
**Estimated Total Time**: 20 hours (~2 weeks part-time)
