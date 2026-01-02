# Phase III AI Chatbot Agent

## Purpose
Expert agent for developing the AI-powered todo chatbot with MCP server integration (Phase III).

## Responsibilities
- Build OpenAI ChatKit UI for conversational interface
- Implement OpenAI Agents SDK for AI orchestration
- Create MCP server with Official MCP SDK (Python)
- Expose task operations as MCP tools
- Implement stateless chat endpoint with database persistence
- Enable natural language task management

## Technology Stack

### Frontend (Chatbot UI)
- **Framework**: OpenAI ChatKit
- **Integration**: Connects to backend chat endpoint
- **Deployment**: Vercel (alongside Phase II frontend)

### Backend (AI Agent)
- **AI Framework**: OpenAI Agents SDK
- **MCP**: Official MCP SDK (Python)
- **Backend**: FastAPI (extends Phase II)
- **Database**: Same Neon PostgreSQL (conversations + messages tables)

### MCP Server
- **SDK**: Official MCP SDK (Python)
- **Tools**: add_task, list_tasks, complete_task, delete_task, update_task
- **Architecture**: Stateless, database-backed

## Key Directories
```
├── frontend/
│   ├── app/chat/          # ChatKit UI integration
│   └── components/chat/   # Chat components
├── backend/
│   ├── app/
│   │   ├── mcp/           # MCP server and tools
│   │   │   ├── server.py  # MCP server
│   │   │   └── tools.py   # Task tools
│   │   ├── routes/
│   │   │   └── chat.py    # Chat endpoint
│   │   └── models.py      # + conversations, messages models
└── specs/phase3-chatbot/  # Specifications (to be created)
```

## Database Schema Extensions

### conversations
```sql
id          SERIAL PRIMARY KEY
user_id     TEXT REFERENCES users(id)
created_at  TIMESTAMP DEFAULT NOW()
updated_at  TIMESTAMP DEFAULT NOW()
```

### messages
```sql
id                SERIAL PRIMARY KEY
conversation_id   INTEGER REFERENCES conversations(id)
user_id           TEXT REFERENCES users(id)
role             TEXT CHECK (role IN ('user', 'assistant'))
content          TEXT NOT NULL
created_at       TIMESTAMP DEFAULT NOW()
```

**Indexes**: messages.conversation_id, conversations.user_id

## MCP Tools Specification

All task operations exposed as MCP tools:

### add_task
```python
{
    "name": "add_task",
    "description": "Create a new todo task",
    "parameters": {
        "user_id": "string",
        "title": "string (1-200 chars)",
        "description": "string (optional, max 1000 chars)"
    },
    "returns": {
        "task_id": "integer",
        "message": "string"
    }
}
```

### list_tasks
```python
{
    "name": "list_tasks",
    "description": "Retrieve all tasks for a user",
    "parameters": {
        "user_id": "string",
        "status_filter": "string (optional: 'all'|'completed'|'active')"
    },
    "returns": {
        "tasks": "array of task objects"
    }
}
```

### complete_task
```python
{
    "name": "complete_task",
    "description": "Mark a task as complete or incomplete",
    "parameters": {
        "user_id": "string",
        "task_id": "integer",
        "completed": "boolean"
    },
    "returns": {
        "message": "string"
    }
}
```

### delete_task
```python
{
    "name": "delete_task",
    "description": "Remove a task",
    "parameters": {
        "user_id": "string",
        "task_id": "integer"
    },
    "returns": {
        "message": "string"
    }
}
```

### update_task
```python
{
    "name": "update_task",
    "description": "Modify task title or description",
    "parameters": {
        "user_id": "string",
        "task_id": "integer",
        "title": "string (optional)",
        "description": "string (optional)"
    },
    "returns": {
        "message": "string"
    }
}
```

## Chat Endpoint Architecture

### Stateless Design
```
User → ChatKit UI → POST /api/chat
                      ↓
              OpenAI Agents SDK
                      ↓
              MCP Tools (task operations)
                      ↓
              Database (persist conversation)
                      ↓
              Response → User
```

### Chat Endpoint
```python
POST /api/chat
{
    "user_id": "string",
    "conversation_id": "integer (optional)",
    "message": "string"
}

Response:
{
    "conversation_id": "integer",
    "message": "string",
    "tasks_modified": ["array of task IDs affected"]
}
```

## Natural Language Examples

User can interact conversationally:

- **Add task**: "Add a task to buy groceries"
- **List tasks**: "Show me all my tasks" or "What do I need to do?"
- **Complete**: "Mark task 5 as done" or "Complete buy groceries"
- **Delete**: "Delete task 3" or "Remove the meeting task"
- **Update**: "Change task 2 title to 'Team standup'"
- **Mixed**: "Add a task to call mom and show me all incomplete tasks"

## MCP Server Implementation

### Server Setup
```python
from mcp import MCPServer
from app.mcp.tools import register_task_tools

server = MCPServer(name="todo-mcp-server")
register_task_tools(server)

if __name__ == "__main__":
    server.run()
```

### Tool Registration
```python
@server.tool()
async def add_task(user_id: str, title: str, description: str = ""):
    # Validate user_id
    # Create task in database
    # Return task_id and success message
    pass
```

## OpenAI Agents SDK Integration

### Agent Configuration
```python
from openai import OpenAI
from app.mcp.server import get_mcp_tools

client = OpenAI(api_key=OPENAI_API_KEY)

agent = client.beta.agents.create(
    name="Todo Assistant",
    instructions="""You are a helpful todo list assistant.
    Help users manage their tasks using the available tools.
    Be conversational and friendly.""",
    tools=get_mcp_tools(),
    model="gpt-4"
)
```

### Chat Flow
```python
async def handle_chat(user_id: str, message: str, conversation_id: int = None):
    # 1. Create or load conversation from database
    # 2. Add user message to messages table
    # 3. Call OpenAI Agents SDK with conversation history
    # 4. Agent orchestrates MCP tool calls
    # 5. Persist assistant response to messages table
    # 6. Return response to user
```

## Development Workflow

### Setup
```bash
# Install OpenAI SDK
uv add openai

# Install MCP SDK
uv add mcp

# Set OpenAI API key in .env
OPENAI_API_KEY=sk-...
```

### Run MCP Server (standalone)
```bash
cd backend
uv run python -m app.mcp.server
```

### Run Chat Endpoint (development)
```bash
cd backend
uv run uvicorn app.main:app --reload
```

### Test ChatKit UI
```bash
cd frontend
npm run dev
# Navigate to /chat
```

## Testing Strategy

### Unit Tests
- Test each MCP tool individually
- Mock database calls
- Verify input validation
- Test error handling

### Integration Tests
- Test OpenAI Agents SDK with MCP tools
- Verify tool calling works end-to-end
- Test conversation persistence
- Verify multi-turn conversations

### Manual Testing
1. **Add task via chat**: "Add a task to review code"
2. **List tasks**: "What are my tasks?"
3. **Complete task**: "Mark the review code task as done"
4. **Update task**: "Change it to code review with team"
5. **Delete task**: "Delete that task"
6. **Multi-step**: "Add three tasks: email, meeting, and lunch. Then show me all tasks."

## Security Considerations
- ✅ Validate user_id in all MCP tools (prevent cross-user access)
- ✅ JWT authentication for chat endpoint
- ✅ Rate limiting on chat endpoint (prevent abuse)
- ✅ Sanitize user inputs before passing to AI
- ✅ No sensitive data in conversation logs
- ✅ OpenAI API key stored securely (.env)

## Performance Requirements
- Chat response: < 3 seconds (including AI processing)
- MCP tool execution: < 100ms each
- Database queries: Indexed and optimized
- Conversation history: Load only recent messages (e.g., last 50)

## Success Criteria
- [ ] MCP server running and exposing all 5 task tools
- [ ] OpenAI Agents SDK integrated
- [ ] ChatKit UI functional and connected
- [ ] Natural language task operations working
- [ ] Conversations persist to database
- [ ] Multi-turn conversations maintain context
- [ ] All task operations work via chat
- [ ] User data isolated (can't access others' tasks)
- [ ] Chat endpoint stateless (server restarts don't lose data)

## Common Issues & Solutions

### Tool Calling Not Working
- Verify MCP tools registered correctly
- Check OpenAI Agents SDK tool schema format
- Ensure function signatures match tool definitions

### Conversation Context Lost
- Load recent messages from database on each request
- Pass full conversation history to OpenAI API
- Don't rely on server-side sessions

### Slow Responses
- Optimize database queries (add indexes)
- Limit conversation history (last 50 messages)
- Use OpenAI streaming for faster perceived performance

## Related Agents
- `phase2-web.md` - Web app foundation (extends this)
- `testing.md` - Testing strategies
- `deployment.md` - Deploying MCP server

## Commands to Use
- `/sp.specify` - Create Phase III spec
- `/sp.plan` - Design chatbot architecture
- `/sp.tasks` - Break down MCP server tasks
- `/sp.implement` - Execute implementation
- `/sp.phr` - Create Prompt History Record
- `/sp.adr` - Document MCP architecture decisions

---

**Remember**: Phase III adds AI capabilities on top of Phase II. Keep MCP server stateless and database-backed for Phase IV Kubernetes deployment.
