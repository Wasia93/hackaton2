# Skill: phase3.chat

## Description
Start Phase III chatbot with MCP server

## Usage
```
/phase3.chat
```

## What It Does
- Starts MCP server (port 8001)
- Starts Phase II services (frontend + backend)
- Enables chatbot UI at /chat route
- Displays all service URLs

## Commands Executed
```bash
# Terminal 1: MCP Server
cd backend && uv run python -m app.mcp.server

# Terminal 2: Backend API
cd backend && uv run uvicorn app.main:app --reload

# Terminal 3: Frontend (with ChatKit)
cd frontend && npm run dev
```

## Prerequisites
- Phase III implementation complete
- OpenAI API key configured
- MCP server implemented
- ChatKit UI integrated
- Database with conversations + messages tables

## Access URLs
- Chatbot UI: http://localhost:3000/chat
- MCP Server: http://localhost:8001
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Variables Required

### Backend (.env)
```
DATABASE_URL=postgresql://...@neon.tech/db
JWT_SECRET=your-secret-key
OPENAI_API_KEY=sk-...
MCP_SERVER_URL=http://localhost:8001
```

## MCP Tools Available
- `add_task` - Create new task
- `list_tasks` - Retrieve user's tasks
- `complete_task` - Mark task complete/incomplete
- `delete_task` - Remove task
- `update_task` - Modify task details

## Testing Natural Language
Try these commands in chat:
- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task 5 as complete"
- "Delete the groceries task"
- "Change task 2 to 'Team meeting at 3pm'"

## Related Files
- `backend/app/mcp/` - MCP server and tools
- `frontend/app/chat/` - ChatKit UI
- `specs/phase3-chatbot/` - Phase III specifications

## Related Agents
- `.claude/agents/phase3-chatbot.md`
- `.claude/agents/phase2-web.md`

---

**Tip**: Use this skill to test AI-powered todo management with natural language.
