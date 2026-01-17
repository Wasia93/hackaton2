# Phase III: AI Chatbot with MCP - Specification

**Feature**: Natural Language Todo Management via AI Chatbot
**Phase**: Phase III - AI Chatbot Integration
**Status**: Draft
**Created**: 2026-01-13
**Updated**: 2026-01-13

---

## 1. Overview

Transform the Phase II web application by adding an AI-powered chatbot interface that allows users to manage todos through natural language conversations using OpenAI Agents SDK and MCP (Model Context Protocol) tools.

### Purpose
- Enable natural language task management ("Add buy groceries to my list")
- Provide conversational AI interface alongside existing web UI
- Demonstrate MCP server integration for tool-based AI interactions
- Persist conversation history for context continuity
- Maintain stateless architecture with database-backed sessions

### Constraints
- **No manual coding** - All code generated via Claude Code using this spec
- **Spec-Driven Development** - Follow Specify → Plan → Tasks → Implement
- **Stateless architecture** - All state persists in PostgreSQL database
- **Phase II compatibility** - Web UI and chatbot share same backend API
- **OpenAI Agents SDK** - Use official SDK for agent orchestration
- **Official MCP SDK** - Use Python MCP SDK for tool definitions

### Key Changes from Phase II

| Aspect | Phase II | Phase III |
|--------|----------|-----------|
| Interface | Web UI only | Web UI + Chatbot |
| Interaction | Direct API calls | Natural language + MCP tools |
| AI Integration | None | OpenAI Agents SDK |
| Tool Protocol | RESTful API | MCP Server |
| Chat UI | None | OpenAI ChatKit |
| Conversations | N/A | Database-persisted |

---

## 2. User Journeys

### UJ-1: Start Conversation with Chatbot
**As a logged-in user**
**I want to** open the chatbot interface
**So that** I can manage my tasks using natural language

**Flow**:
1. User clicks "Chat Assistant" button on dashboard
2. Chatbot interface opens (modal or sidebar)
3. System loads user's conversation history (if exists)
4. Welcome message displayed: "Hi! I can help you manage your tasks. What would you like to do?"
5. User can type messages or use suggested prompts

**Acceptance Criteria**:
- ✅ Chatbot interface accessible from dashboard
- ✅ Previous conversation loaded if exists
- ✅ New conversation created if first time
- ✅ User ID associated with conversation
- ✅ Welcome message shown

---

### UJ-2: Create Task via Natural Language
**As a user**
**I want to** create a task by telling the chatbot
**So that** I can quickly add tasks without forms

**Flow**:
1. User types: "Add buy groceries to my list"
2. Message sent to backend chat endpoint
3. OpenAI agent interprets intent
4. Agent calls MCP tool `create_task` with extracted title
5. Task created in database
6. Agent responds: "✓ Added 'Buy groceries' to your task list"
7. Response shown in chat UI

**Acceptance Criteria**:
- ✅ Natural language interpreted correctly
- ✅ Task created with user_id
- ✅ Task appears in web UI immediately
- ✅ Confirmation message shown in chat
- ✅ Conversation persisted to database

**Example Prompts**:
- "Add buy milk to my tasks"
- "Remind me to call dentist"
- "Create a task: finish hackathon project"
- "I need to buy groceries tomorrow"

---

### UJ-3: View Tasks via Conversation
**As a user**
**I want to** ask the chatbot to show my tasks
**So that** I can review them conversationally

**Flow**:
1. User types: "What are my tasks?" or "Show me my todo list"
2. Agent calls MCP tool `list_tasks`
3. Tasks retrieved from database (filtered by user_id)
4. Agent formats response with task list
5. Response: "You have 3 tasks:\n1. ✓ Buy groceries (completed)\n2. ✗ Call dentist (pending)\n3. ✗ Finish project (pending)"

**Acceptance Criteria**:
- ✅ Query interpreted correctly
- ✅ Only user's tasks shown
- ✅ Tasks formatted clearly
- ✅ Completion status indicated
- ✅ Handles empty list gracefully

**Example Prompts**:
- "Show my tasks"
- "What do I need to do?"
- "List all my todos"
- "What's on my task list?"

---

### UJ-4: Update Task via Natural Language
**As a user**
**I want to** modify a task by describing the change
**So that** I can update tasks without clicking through UI

**Flow**:
1. User types: "Change 'buy groceries' to 'buy groceries and milk'"
2. Agent identifies task by title match
3. Agent calls MCP tool `update_task` with task_id and new title
4. Task updated in database
5. Agent responds: "✓ Updated task to 'Buy groceries and milk'"

**Acceptance Criteria**:
- ✅ Task identified correctly from description
- ✅ Update applied successfully
- ✅ Changes reflected in web UI
- ✅ Confirmation message shown
- ✅ Handles ambiguous matches (asks for clarification)

**Example Prompts**:
- "Rename 'call dentist' to 'call dentist at 2pm'"
- "Update the groceries task to include milk"
- "Change my first task description"

---

### UJ-5: Complete Task via Conversation
**As a user**
**I want to** mark tasks as complete by telling the chatbot
**So that** I can quickly update task status

**Flow**:
1. User types: "Mark 'buy groceries' as done" or "I finished the groceries task"
2. Agent identifies task
3. Agent calls MCP tool `complete_task`
4. Task marked as completed in database
5. Agent responds: "✓ Marked 'Buy groceries' as complete! Great job!"

**Acceptance Criteria**:
- ✅ Task identified from natural language
- ✅ Completion status toggled
- ✅ Changes synced to web UI
- ✅ Celebratory confirmation message
- ✅ Can also mark as incomplete

**Example Prompts**:
- "Mark buy milk as done"
- "I completed the dentist task"
- "Finished groceries"
- "Check off the first task"

---

### UJ-6: Delete Task via Conversation
**As a user**
**I want to** remove tasks by asking the chatbot
**So that** I can clean up my list conversationally

**Flow**:
1. User types: "Delete the groceries task"
2. Agent identifies task
3. Agent asks for confirmation: "Are you sure you want to delete 'Buy groceries'?"
4. User confirms: "Yes" or "Delete it"
5. Agent calls MCP tool `delete_task`
6. Task removed from database
7. Agent responds: "✓ Deleted 'Buy groceries'"

**Acceptance Criteria**:
- ✅ Task identified correctly
- ✅ Confirmation requested
- ✅ Deletion only after confirmation
- ✅ Task removed from web UI
- ✅ Confirmation message shown

**Example Prompts**:
- "Remove the milk task"
- "Delete all completed tasks"
- "Get rid of the groceries reminder"

---

### UJ-7: Get Task Statistics
**As a user**
**I want to** ask about my task progress
**So that** I can understand my productivity

**Flow**:
1. User types: "How many tasks do I have?" or "What's my progress?"
2. Agent calls MCP tool `list_tasks`
3. Agent calculates statistics
4. Agent responds: "You have 5 tasks total: 2 completed (40%), 3 pending (60%)"

**Acceptance Criteria**:
- ✅ Statistics calculated correctly
- ✅ Response formatted clearly
- ✅ Percentage shown
- ✅ Motivational language used

**Example Prompts**:
- "How am I doing?"
- "Task summary"
- "Show my stats"
- "How many completed tasks?"

---

### UJ-8: Context-Aware Conversations
**As a user**
**I want to** have multi-turn conversations with context
**So that** I can interact naturally without repeating information

**Flow**:
1. User: "Show my tasks"
2. Bot: Lists 3 tasks
3. User: "Mark the first one as done" (refers to previous response)
4. Bot identifies task from conversation context
5. Task marked complete
6. Bot: "✓ Marked 'Buy groceries' as complete!"

**Acceptance Criteria**:
- ✅ Conversation history maintained
- ✅ References resolved correctly
- ✅ Context persists across page refreshes
- ✅ Context cleared on explicit request
- ✅ Context limited to current user

---

## 3. Functional Requirements

### FR-1: MCP Server Implementation

**Priority**: CRITICAL
**Dependencies**: Phase II backend

**Requirements**:
- Implement MCP server using Official Python MCP SDK
- Expose all task CRUD operations as MCP tools
- Each tool has clear schema with input/output types
- Tools are stateless and interact with database
- Tools enforce user_id isolation (security)

**MCP Tools to Implement**:

1. **`create_task`**
   - Input: `{ user_id: string, title: string, description?: string }`
   - Output: `{ id: number, title: string, created_at: string }`
   - Description: "Create a new task for the user"

2. **`list_tasks`**
   - Input: `{ user_id: string, filter?: "all" | "completed" | "pending" }`
   - Output: `{ tasks: Task[] }`
   - Description: "List all tasks for the user with optional filter"

3. **`get_task`**
   - Input: `{ user_id: string, task_id: number }`
   - Output: `{ task: Task }`
   - Description: "Get a specific task by ID"

4. **`update_task`**
   - Input: `{ user_id: string, task_id: number, title?: string, description?: string }`
   - Output: `{ task: Task }`
   - Description: "Update task title and/or description"

5. **`complete_task`**
   - Input: `{ user_id: string, task_id: number }`
   - Output: `{ task: Task }`
   - Description: "Mark a task as complete"

6. **`delete_task`**
   - Input: `{ user_id: string, task_id: number }`
   - Output: `{ success: boolean }`
   - Description: "Delete a task permanently"

7. **`search_tasks`**
   - Input: `{ user_id: string, query: string }`
   - Output: `{ tasks: Task[] }`
   - Description: "Search tasks by title or description"

**MCP Server Configuration**:
```python
# mcp_server.py
from mcp import Server
from mcp.types import Tool

server = Server("todo-mcp-server")

@server.tool("create_task")
async def create_task(user_id: str, title: str, description: str = ""):
    # Call task service to create task
    pass
```

---

### FR-2: OpenAI Agents SDK Integration

**Priority**: CRITICAL
**Dependencies**: FR-1

**Requirements**:
- Use OpenAI Agents SDK (beta) for agent orchestration
- Agent has access to all MCP tools
- Agent interprets natural language and selects appropriate tool
- Agent maintains conversation context
- Agent provides helpful, friendly responses

**Agent Configuration**:
```python
from openai import OpenAI
from openai.agents import Agent

agent = Agent(
    name="Todo Assistant",
    instructions="""
    You are a helpful todo list assistant. You help users manage their tasks through natural conversation.

    Always:
    - Be friendly and encouraging
    - Confirm actions clearly
    - Celebrate task completions
    - Ask for clarification if intent is ambiguous
    - Format task lists clearly with checkboxes (✓ / ✗)

    Available tools:
    - create_task: Add new tasks
    - list_tasks: Show all tasks
    - update_task: Modify existing tasks
    - complete_task: Mark tasks as done
    - delete_task: Remove tasks
    - search_tasks: Find specific tasks
    """,
    model="gpt-4o",
    tools=mcp_tools  # MCP tools injected here
)
```

---

### FR-3: Conversation Persistence

**Priority**: CRITICAL
**Dependencies**: Phase II database

**Requirements**:
- All conversations stored in PostgreSQL database
- Each user can have multiple conversations
- Messages stored with role (user/assistant), content, timestamp
- Conversation history loaded on chatbot open
- Context maintained across page refreshes
- Old conversations archived but accessible

**Database Schema**:

**conversations**
```sql
CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(200),  -- Auto-generated from first message
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_user_conversations (user_id, updated_at DESC)
);
```

**messages**
```sql
CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
  content TEXT NOT NULL,
  tool_calls JSONB,  -- If assistant used tools
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_conversation_messages (conversation_id, created_at ASC)
);
```

---

### FR-4: Stateless Chat Endpoint

**Priority**: CRITICAL
**Dependencies**: FR-2, FR-3

**Requirements**:
- Single `/api/chat` endpoint handles all chat interactions
- Endpoint is stateless (no server-side sessions)
- Conversation ID passed in request
- Messages retrieved from database
- Agent processes message with full conversation context
- Response saved to database before returning

**API Endpoint**:
```typescript
POST /api/chat
Authorization: Bearer <jwt_token>

Request:
{
  "conversation_id": 123,  // null for new conversation
  "message": "Add buy groceries to my list"
}

Response:
{
  "conversation_id": 123,
  "message": {
    "id": 456,
    "role": "assistant",
    "content": "✓ Added 'Buy groceries' to your task list",
    "tool_calls": [
      {
        "tool": "create_task",
        "arguments": { "title": "Buy groceries" },
        "result": { "id": 789 }
      }
    ],
    "created_at": "2026-01-13T10:30:00Z"
  }
}
```

---

### FR-5: ChatKit UI Integration

**Priority**: CRITICAL
**Dependencies**: Phase II frontend

**Requirements**:
- Use OpenAI ChatKit React component library
- Chatbot accessible from dashboard (modal or sidebar)
- Chat interface shows conversation history
- Messages styled as user/assistant bubbles
- Typing indicator during agent processing
- Input field with send button
- Auto-scroll to latest message
- Responsive design

**UI Components**:
- `ChatbotModal` - Modal overlay with chat interface
- `ChatMessage` - Individual message bubble
- `ChatInput` - Text input with send button
- `ConversationList` - Sidebar with past conversations
- `TypingIndicator` - Shows when agent is thinking

---

### FR-6: Task Intent Recognition

**Priority**: HIGH
**Dependencies**: FR-2

**Requirements**:
- Agent recognizes common task operations from natural language
- Handles variations in phrasing
- Extracts task details (title, description)
- Asks for clarification when ambiguous
- Supports colloquial language

**Intent Patterns**:

**Create Task**:
- "Add [task] to my list"
- "Remind me to [task]"
- "Create a task: [task]"
- "I need to [task]"
- "Don't let me forget to [task]"

**List Tasks**:
- "Show my tasks"
- "What do I need to do?"
- "List todos"
- "What's on my list?"

**Complete Task**:
- "Mark [task] as done"
- "I finished [task]"
- "Completed [task]"
- "Check off [task]"

**Update Task**:
- "Change [task] to [new task]"
- "Rename [task]"
- "Update [task]"

**Delete Task**:
- "Delete [task]"
- "Remove [task]"
- "Get rid of [task]"

---

## 4. Non-Functional Requirements

### NFR-1: Performance
- Chat response time < 5 seconds (including LLM latency)
- Conversation history loads in < 1 second
- Database queries optimized with indexes
- MCP tool calls < 200ms each

### NFR-2: Security
- User can only access their own conversations
- MCP tools validate user_id on every call
- JWT token required for chat endpoint
- Conversation data encrypted at rest
- No conversation data leaks between users

### NFR-3: Scalability
- Stateless architecture allows horizontal scaling
- Database connection pooling
- OpenAI API rate limiting handled gracefully
- Concurrent conversations supported

### NFR-4: Usability
- Natural language processing feels intuitive
- Agent responses are clear and friendly
- Error messages are helpful
- Typing indicator provides feedback
- Chat history helps context retention

### NFR-5: Reliability
- Graceful handling of OpenAI API errors
- Fallback messages when LLM unavailable
- Conversation state persisted on every message
- No data loss on server restart

---

## 5. Acceptance Criteria

### AC-1: MCP Server
- ✅ MCP server running and accessible
- ✅ All 7 tools implemented
- ✅ Tools have correct schemas
- ✅ Tools enforce user_id isolation
- ✅ Tools return proper error codes

### AC-2: OpenAI Agent
- ✅ Agent interprets natural language correctly
- ✅ Agent selects appropriate MCP tools
- ✅ Agent maintains conversation context
- ✅ Agent provides friendly responses
- ✅ Agent handles errors gracefully

### AC-3: Chat Endpoint
- ✅ POST /api/chat endpoint works
- ✅ Requires authentication
- ✅ Saves messages to database
- ✅ Returns agent response
- ✅ Creates new conversation if needed

### AC-4: Conversation Persistence
- ✅ Conversations saved to database
- ✅ Messages linked to conversations
- ✅ History loaded on chatbot open
- ✅ Context maintained across refreshes
- ✅ Old conversations accessible

### AC-5: ChatKit UI
- ✅ Chatbot opens from dashboard
- ✅ Messages displayed correctly
- ✅ User can send messages
- ✅ Typing indicator shows
- ✅ Auto-scrolls to latest
- ✅ Responsive on mobile

### AC-6: Task Operations via Chat
- ✅ User can create tasks via chat
- ✅ User can list tasks via chat
- ✅ User can update tasks via chat
- ✅ User can complete tasks via chat
- ✅ User can delete tasks via chat
- ✅ All operations reflected in web UI

### AC-7: Intent Recognition
- ✅ Agent understands various phrasings
- ✅ Agent extracts task details correctly
- ✅ Agent asks for clarification when needed
- ✅ Agent handles typos reasonably

### AC-8: Data Isolation
- ✅ User A cannot see User B's conversations
- ✅ User A cannot modify User B's tasks via chat
- ✅ MCP tools validate user_id
- ✅ Chat endpoint enforces authorization

---

## 6. Out of Scope (Phase III)

The following features are explicitly **excluded** from Phase III:

- ❌ Voice input/output (nice-to-have)
- ❌ Multi-language support (English only)
- ❌ Conversation sharing between users
- ❌ Task priorities via chat (Phase II feature, not yet in chat)
- ❌ Task tags via chat (not in Phase II)
- ❌ Due dates and reminders via chat (Phase V)
- ❌ File attachments in chat
- ❌ Rich text formatting in messages
- ❌ Custom agent personalities
- ❌ Fine-tuned models (use GPT-4 out-of-the-box)

---

## 7. Dependencies

### External Services
- **OpenAI API** - GPT-4 for agent intelligence
- **Neon PostgreSQL** - Database (already from Phase II)
- **Vercel** - Frontend hosting (already from Phase II)
- **Backend Hosting** - Railway/Render (already from Phase II)

### Frontend Dependencies
- OpenAI ChatKit (React component library)
- Existing Phase II frontend stack

### Backend Dependencies
- OpenAI Python SDK (openai>=1.0.0)
- OpenAI Agents SDK (beta)
- Official MCP SDK (mcp>=0.1.0)
- Existing Phase II backend stack

---

## 8. Risks and Assumptions

### Risks
- **R-1**: OpenAI API rate limits (mitigated by error handling, retry logic)
- **R-2**: LLM hallucinations (mitigated by tool-based actions, not free-form)
- **R-3**: OpenAI Agents SDK is in beta (mitigated by fallback to direct API calls)
- **R-4**: MCP protocol adoption (mitigated by using official SDK)
- **R-5**: Response latency from LLM (acceptable for chat use case)

### Assumptions
- **A-1**: OpenAI API costs acceptable for development (<$10/month)
- **A-2**: GPT-4 sufficient for task intent recognition
- **A-3**: Users comfortable with conversational AI
- **A-4**: English language only (no i18n required)
- **A-5**: Internet connection available (no offline mode)
- **A-6**: Phase II backend and database functional

---

## 9. Success Metrics

Phase III is successful when:
- ✅ MCP server running with all 7 tools
- ✅ OpenAI agent interprets task intents correctly
- ✅ Users can perform all CRUD operations via chat
- ✅ Conversations persist to database
- ✅ ChatKit UI integrated and functional
- ✅ Task changes from chat reflected in web UI
- ✅ Data isolation enforced for all chat operations
- ✅ All acceptance criteria pass
- ✅ Code generated via Claude Code (no manual coding)
- ✅ Follows constitution principles

---

## 10. References

- [Phase II Spec](../phase2-web-app/spec.md) - Web app requirements
- [Phase I Spec](../phase1-console-app/spec.md) - Console app foundation
- [Constitution](../../.specify/memory/constitution.md) - Project principles
- [AGENTS.md](../../AGENTS.md) - Agent workflow instructions
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents) - Agent docs
- [MCP Protocol](https://modelcontextprotocol.io/) - MCP specification
- [OpenAI ChatKit](https://github.com/openai/chatkit) - UI component library

---

**Spec Version**: 1.0.0
**Approved By**: [Pending approval]
**Approval Date**: [Pending]
**Next Step**: Create plan.md (HOW to build)
