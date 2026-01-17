# Phase III: AI Chatbot with MCP - Technical Plan

**Feature**: Natural Language Todo Management via AI Chatbot
**Phase**: Phase III - AI Chatbot Integration
**Status**: Ready for Implementation
**Created**: 2026-01-13
**Updated**: 2026-01-13

**References**:
- [Specification](./spec.md) - WHAT to build
- [Phase II Plan](../phase2-web-app/plan.md) - Web app architecture
- [Constitution](../../.specify/memory/constitution.md) - Project principles

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Phase III: AI Chatbot System                      │
│                                                                      │
│  ┌──────────────────┐                                               │
│  │  Next.js Frontend│                                               │
│  │  + ChatKit UI    │                                               │
│  │  (Vercel)        │                                               │
│  └────────┬─────────┘                                               │
│           │ HTTPS                                                    │
│           ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │           FastAPI Backend (Railway/Render)              │        │
│  │  ┌──────────────┐   ┌─────────────┐   ┌──────────────┐│        │
│  │  │ Phase II API │   │  Chat API   │   │  MCP Server  ││        │
│  │  │ (Tasks CRUD) │   │ Endpoint    │   │  (Tools)     ││        │
│  │  └──────────────┘   └──────┬──────┘   └──────┬───────┘│        │
│  │                             │                  │        │        │
│  │                             ▼                  ▼        │        │
│  │                     ┌───────────────────────────────┐  │        │
│  │                     │   OpenAI Agents SDK           │  │        │
│  │                     │   - Agent Orchestration       │  │        │
│  │                     │   - MCP Tool Integration      │  │        │
│  │                     │   - Context Management        │  │        │
│  │                     └────────────┬──────────────────┘  │        │
│  │                                  │                      │        │
│  │                                  ▼                      │        │
│  │                          ┌──────────────┐              │        │
│  │                          │  OpenAI API  │              │        │
│  │                          │   (GPT-4)    │              │        │
│  │                          └──────────────┘              │        │
│  └──────────────────────────────┬──────────────────────────┘       │
│                                  │                                  │
│                                  ▼                                  │
│                     ┌────────────────────────────┐                 │
│                     │  Neon PostgreSQL           │                 │
│                     │  - tasks                   │                 │
│                     │  - conversations (NEW)     │                 │
│                     │  - messages (NEW)          │                 │
│                     └────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow: Chat Message Processing

```
User types message
    │
    ▼
ChatKit UI component
    │
    ▼
POST /api/chat
    │
    ├─ Extract user_id from JWT
    ├─ Load conversation history from DB
    ├─ Create user message in DB
    │
    ▼
OpenAI Agent (with MCP tools)
    │
    ├─ Interpret intent
    ├─ Determine appropriate tool(s)
    ├─ Execute MCP tool call(s)
    │   │
    │   ▼
    │   MCP Server
    │   │
    │   ├─ create_task(user_id, title)
    │   ├─ list_tasks(user_id)
    │   ├─ complete_task(user_id, task_id)
    │   └─ etc...
    │       │
    │       ▼
    │   Task Service (Phase II logic)
    │       │
    │       ▼
    │   Database UPDATE
    │
    ├─ Generate response text
    │
    ▼
Save assistant message to DB
    │
    ▼
Return response to frontend
    │
    ▼
Display in ChatKit UI
    │
    ▼
Update task list in background (if needed)
```

---

## 2. Technology Stack

### Backend Additions (Phase III)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| AI Agent | OpenAI Agents SDK (beta) | Agent orchestration & tool calling |
| MCP Server | Official MCP SDK (Python) | Tool protocol implementation |
| LLM | OpenAI GPT-4 (gpt-4o) | Natural language understanding |
| API Client | OpenAI Python SDK (>=1.0.0) | OpenAI API integration |

### Frontend Additions (Phase III)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Chat UI | OpenAI ChatKit (React) | Pre-built chat components |
| State Mgmt | React hooks (useState, useEffect) | Chat state management |
| WebSockets | (Optional) | Real-time message streaming |

### Database Additions (Phase III)

- **conversations** table - User chat sessions
- **messages** table - Individual chat messages

---

## 3. Database Schema Changes

### New Tables

#### conversations
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),                   -- Auto-generated from first message
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_user_conversations (user_id, updated_at DESC)
);
```

#### messages
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,           -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tool_calls JSONB,                    -- Store tool call details if any
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_conversation_messages (conversation_id, created_at ASC)
);
```

**JSONB Structure for tool_calls**:
```json
[
  {
    "id": "call_abc123",
    "tool": "create_task",
    "arguments": {
      "user_id": "user-uuid",
      "title": "Buy groceries"
    },
    "result": {
      "id": 789,
      "title": "Buy groceries",
      "created_at": "2026-01-13T10:30:00Z"
    }
  }
]
```

### SQLModel Classes

```python
# app/models/conversation.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)
    title: str = Field(default="New Conversation", max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# app/models/message.py
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Any

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    tool_calls: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## 4. MCP Server Implementation

### 4.1 MCP Tool Definitions

Each tool follows this structure:

```python
from mcp import Tool
from pydantic import BaseModel, Field

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

create_task_tool = Tool(
    name="create_task",
    description="Create a new task for the user",
    input_schema=CreateTaskInput.schema(),
    handler=handle_create_task
)

async def handle_create_task(input: CreateTaskInput) -> CreateTaskOutput:
    # Call existing Phase II task service
    from app.services.task_service import TaskService
    from app.core.database import get_session

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
```

### 4.2 Complete Tool List

1. **create_task** - Create new task
2. **list_tasks** - Get all user's tasks (with optional filter)
3. **get_task** - Get specific task by ID
4. **update_task** - Update task title/description
5. **complete_task** - Toggle task completion status
6. **delete_task** - Delete a task
7. **search_tasks** - Search tasks by keyword

### 4.3 MCP Server Setup

```python
# app/mcp_server.py
from mcp import Server
from app.mcp_tools import (
    create_task_tool,
    list_tasks_tool,
    get_task_tool,
    update_task_tool,
    complete_task_tool,
    delete_task_tool,
    search_tasks_tool
)

mcp_server = Server("todo-mcp-server")

# Register all tools
mcp_server.add_tool(create_task_tool)
mcp_server.add_tool(list_tasks_tool)
mcp_server.add_tool(get_task_tool)
mcp_server.add_tool(update_task_tool)
mcp_server.add_tool(complete_task_tool)
mcp_server.add_tool(delete_task_tool)
mcp_server.add_tool(search_tasks_tool)

def get_mcp_tools():
    """Return list of tools for OpenAI agent"""
    return [
        create_task_tool,
        list_tasks_tool,
        get_task_tool,
        update_task_tool,
        complete_task_tool,
        delete_task_tool,
        search_tasks_tool
    ]
```

---

## 5. OpenAI Agent Configuration

### 5.1 Agent System Instructions

```python
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
```

### 5.2 Agent Initialization

```python
# app/services/ai_agent_service.py
from openai import OpenAI
from openai.agents import Agent
from app.core.config import settings
from app.mcp_server import get_mcp_tools

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def create_agent():
    """Create and configure the OpenAI agent"""
    agent = Agent(
        name="Todo Assistant",
        instructions=AGENT_INSTRUCTIONS,
        model="gpt-4o",  # GPT-4 Optimized
        tools=get_mcp_tools(),
        client=client
    )
    return agent

# Singleton instance
todo_agent = create_agent()
```

### 5.3 Message Processing

```python
async def process_chat_message(
    user_id: str,
    conversation_id: int,
    message_content: str,
    conversation_history: list
) -> dict:
    """
    Process a user message through the agent

    Args:
        user_id: Authenticated user ID
        conversation_id: Current conversation ID
        message_content: User's message
        conversation_history: Previous messages for context

    Returns:
        {
            "content": "Agent's response text",
            "tool_calls": [...],  # Tools the agent used
        }
    """

    # Build messages list for agent (with history)
    messages = conversation_history + [
        {"role": "user", "content": message_content}
    ]

    # Inject user_id into tool call context
    # (agent will pass this to all MCP tools)
    tool_context = {"user_id": user_id}

    # Run agent
    response = await todo_agent.run(
        messages=messages,
        context=tool_context
    )

    return {
        "content": response.content,
        "tool_calls": response.tool_calls
    }
```

---

## 6. Chat API Endpoint

### 6.1 Endpoint Specification

```python
# app/api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.auth import get_current_user_id
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None  # null for new conversation
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    message: MessageResponse

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    tool_calls: Optional[list] = None
    created_at: str

@router.post("/", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Send a message to the chatbot

    - Creates new conversation if conversation_id is null
    - Loads conversation history
    - Processes message through OpenAI agent
    - Saves user and assistant messages to database
    - Returns assistant's response
    """

    chat_service = ChatService(session, user_id)

    result = await chat_service.process_message(
        conversation_id=request.conversation_id,
        message_content=request.message
    )

    return ChatResponse(
        conversation_id=result["conversation_id"],
        message=MessageResponse(
            id=result["message"]["id"],
            role=result["message"]["role"],
            content=result["message"]["content"],
            tool_calls=result["message"]["tool_calls"],
            created_at=result["message"]["created_at"]
        )
    )
```

### 6.2 Chat Service Layer

```python
# app/services/chat_service.py
from sqlmodel import Session, select
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.ai_agent_service import process_chat_message
from datetime import datetime

class ChatService:
    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id

    async def process_message(
        self,
        conversation_id: Optional[int],
        message_content: str
    ) -> dict:
        """Process a chat message and return response"""

        # Get or create conversation
        if conversation_id is None:
            conversation = self._create_conversation()
        else:
            conversation = self._get_conversation(conversation_id)
            if not conversation:
                raise ValueError("Conversation not found")

        # Load conversation history
        history = self._get_conversation_history(conversation.id)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=message_content
        )
        self.session.add(user_message)
        self.session.commit()
        self.session.refresh(user_message)

        # Process through agent
        agent_response = await process_chat_message(
            user_id=self.user_id,
            conversation_id=conversation.id,
            message_content=message_content,
            conversation_history=history
        )

        # Save assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=agent_response["content"],
            tool_calls=agent_response.get("tool_calls")
        )
        self.session.add(assistant_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        self.session.add(conversation)

        self.session.commit()
        self.session.refresh(assistant_message)

        return {
            "conversation_id": conversation.id,
            "message": {
                "id": assistant_message.id,
                "role": assistant_message.role,
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls,
                "created_at": assistant_message.created_at.isoformat()
            }
        }

    def _create_conversation(self) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(user_id=self.user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def _get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID (must belong to user)"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == self.user_id
        )
        return self.session.exec(statement).first()

    def _get_conversation_history(self, conversation_id: int) -> list:
        """Get all messages in a conversation"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        messages = self.session.exec(statement).all()

        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
```

---

## 7. Frontend Implementation

### 7.1 ChatKit Integration

```typescript
// frontend/components/Chatbot.tsx
"use client"

import { useState, useEffect } from "react"
import { Chat, ChatMessage } from "@openai/chatkit"
import { apiRequest } from "@/lib/api"

interface ChatbotProps {
  isOpen: boolean
  onClose: () => void
}

export default function Chatbot({ isOpen, onClose }: ChatbotProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [conversationId, setConversationId] = useState<number | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  // Load conversation history on mount
  useEffect(() => {
    if (isOpen) {
      loadConversationHistory()
    }
  }, [isOpen])

  const loadConversationHistory = async () => {
    // Load most recent conversation (if exists)
    try {
      const conversations = await apiRequest("/conversations")
      if (conversations.length > 0) {
        const latest = conversations[0]
        setConversationId(latest.id)

        const history = await apiRequest(`/conversations/${latest.id}/messages`)
        setMessages(history.map((msg: any) => ({
          role: msg.role,
          content: msg.content
        })))
      }
    } catch (error) {
      console.error("Failed to load history:", error)
    }
  }

  const handleSendMessage = async (content: string) => {
    // Add user message to UI immediately
    const userMessage: ChatMessage = { role: "user", content }
    setMessages([...messages, userMessage])

    setIsLoading(true)

    try {
      // Send to backend
      const response = await apiRequest("/chat", {
        method: "POST",
        body: JSON.stringify({
          conversation_id: conversationId,
          message: content
        })
      })

      // Update conversation ID if new
      if (!conversationId) {
        setConversationId(response.conversation_id)
      }

      // Add assistant message
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.message.content
      }
      setMessages([...messages, userMessage, assistantMessage])

    } catch (error) {
      console.error("Chat error:", error)
      // Show error message
      setMessages([...messages, userMessage, {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again."
      }])
    } finally {
      setIsLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end justify-end p-4">
      <div className="bg-white rounded-lg shadow-2xl w-96 h-[600px] flex flex-col">
        {/* Header */}
        <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
          <h3 className="font-semibold">Todo Assistant</h3>
          <button onClick={onClose} className="text-white hover:text-gray-200">
            ✕
          </button>
        </div>

        {/* Chat Component */}
        <Chat
          messages={messages}
          onSend={handleSendMessage}
          isLoading={isLoading}
          placeholder="Ask me to create, list, or manage your tasks..."
          className="flex-1"
        />
      </div>
    </div>
  )
}
```

### 7.2 Dashboard Integration

```typescript
// frontend/app/dashboard/page.tsx (additions)
"use client"

import { useState } from "react"
import Chatbot from "@/components/Chatbot"

export default function DashboardPage() {
  const [isChatOpen, setIsChatOpen] = useState(false)

  // ... existing dashboard code ...

  return (
    <div>
      {/* Existing dashboard content */}

      {/* Chat button */}
      <button
        onClick={() => setIsChatOpen(true)}
        className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700"
      >
        💬 Chat
      </button>

      {/* Chatbot */}
      <Chatbot
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
      />
    </div>
  )
}
```

---

## 8. Implementation Strategy

### Phase A: Backend Foundation (Tasks 1-15)
1. Set up MCP server structure
2. Implement all 7 MCP tools
3. Test MCP tools independently
4. Configure OpenAI Agents SDK
5. Create agent with system instructions
6. Add database migrations for conversations/messages
7. Implement conversation service
8. Implement message service
9. Create chat API endpoint
10. Integrate agent with MCP tools
11. Test agent responses
12. Add error handling
13. Implement conversation history loading
14. Add conversation management endpoints
15. Test complete backend flow

### Phase B: Frontend Integration (Tasks 16-25)
1. Install OpenAI ChatKit package
2. Create Chatbot component
3. Implement message display
4. Add message input
5. Connect to chat API
6. Add typing indicator
7. Implement conversation history loading
8. Add conversation list sidebar
9. Style chat interface
10. Add mobile responsiveness

### Phase C: Testing & Polish (Tasks 26-30)
1. Test all task operations via chat
2. Test multi-turn conversations
3. Test context retention
4. Test error handling
5. Add loading states
6. Performance optimization
7. Security audit
8. User acceptance testing
9. Documentation
10. Deployment

---

## 9. Testing Approach

### Unit Tests
- MCP tool handlers (each tool)
- Chat service methods
- Conversation persistence
- Message creation

### Integration Tests
- Agent + MCP tools end-to-end
- Chat endpoint with real agent
- Database persistence
- User isolation

### Manual Testing Scenarios
1. Create task via "Add buy milk"
2. List tasks via "Show my tasks"
3. Update task via "Change milk to chocolate milk"
4. Complete task via "Mark milk as done"
5. Delete task via "Delete the milk task"
6. Multi-turn: "Show tasks" → "Mark first one done"
7. Context retention across page refresh
8. Error recovery when OpenAI API fails

---

## 10. Deployment Considerations

### Environment Variables
```env
# Phase III additions to .env
OPENAI_API_KEY=sk-...
OPENAI_AGENT_MODEL=gpt-4o
MCP_SERVER_PORT=8001
```

### Backend Deployment
- Same Railway/Render deployment as Phase II
- Add OpenAI API key to environment
- Increase memory if needed for MCP server
- Monitor OpenAI API usage and costs

### Frontend Deployment
- Install ChatKit in Vercel build
- No additional configuration needed
- Same deployment process as Phase II

---

## 11. Success Criteria

This plan is successful when:
- ✅ MCP server implemented with all tools
- ✅ OpenAI agent configured and working
- ✅ Chat endpoint functional
- ✅ Conversations persist to database
- ✅ ChatKit UI integrated
- ✅ All task operations work via chat
- ✅ Context maintained across sessions
- ✅ Data isolation enforced
- ✅ Tests pass
- ✅ Documentation complete

---

## 12. Next Steps

1. **Create tasks.md** - Break plan into atomic tasks
2. **Implement backend** - MCP server + chat endpoint
3. **Implement frontend** - ChatKit integration
4. **Test thoroughly** - All scenarios
5. **Deploy** - Same infrastructure as Phase II

---

**Plan Version**: 1.0.0
**Status**: Ready for Task Breakdown
**Created**: 2026-01-13
**Last Updated**: 2026-01-13
