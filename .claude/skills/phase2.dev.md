# Skill: phase2.dev

## Description
Start Phase II development servers (frontend + backend)

## Usage
```
/phase2.dev
```

## What It Does
- Starts Next.js frontend development server (port 3000)
- Starts FastAPI backend development server (port 8000)
- Displays URLs and logs

## Commands Executed
```bash
# Terminal 1: Frontend
cd frontend && npm run dev

# Terminal 2: Backend
cd backend && uv run uvicorn app.main:app --reload
```

## Prerequisites
- Phase II implementation complete
- Frontend dependencies installed (`npm install`)
- Backend dependencies synced (`uv sync`)
- Environment variables configured (.env files)
- Database connection configured (Neon PostgreSQL)

## Access URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Variables Required

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```

### Backend (.env)
```
DATABASE_URL=postgresql://...@neon.tech/db
JWT_SECRET=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

## Related Files
- `frontend/` - Next.js application
- `backend/` - FastAPI application
- `specs/phase2-web-app/` - Phase II specifications

## Related Agents
- `.claude/agents/phase2-web.md`
- `.claude/agents/database.md`

---

**Tip**: Run this skill to start full development environment for Phase II web app.
