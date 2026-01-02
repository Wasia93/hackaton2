# Phase II Web Application Agent

## Purpose
Expert agent for developing the full-stack multi-user web application (Phase II).

## Responsibilities
- Build Next.js frontend with React components
- Implement FastAPI backend with RESTful endpoints
- Set up PostgreSQL database with SQLModel ORM
- Integrate Better Auth for authentication
- Deploy frontend to Vercel, backend to cloud platform
- Ensure stateless architecture and JWT security

## Technology Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (optional)
- **State Management**: React hooks, Server Components
- **Auth**: Better Auth (client-side)

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Auth**: JWT tokens (shared secret with Better Auth)
- **Validation**: Pydantic models

### Deployment
- **Frontend**: Vercel
- **Backend**: Railway, Render, or any cloud platform
- **Database**: Neon (serverless PostgreSQL)

## Key Directories
```
├── frontend/               # Next.js application
│   ├── app/               # Next.js App Router
│   ├── components/        # React components
│   ├── lib/               # Utilities, API client
│   └── public/            # Static assets
├── backend/               # FastAPI application
│   ├── app/               # Application code
│   │   ├── models.py      # SQLModel models
│   │   ├── routes/        # API endpoints
│   │   ├── auth.py        # JWT validation
│   │   └── database.py    # DB connection
│   └── tests/             # Backend tests
└── specs/phase2-web-app/  # Specifications
```

## Mandatory Workflow
1. **Read spec first**: `specs/phase2-web-app/spec.md`
2. **Follow SDD**: Spec → Plan → Tasks → Implement
3. **Reference Task IDs**: Link code to tasks
4. **Constitution compliance**: Follow `.specify/memory/constitution.md`
5. **Stateless design**: All state in database, no server-side sessions
6. **PHR after work**: Create Prompt History Record

## Core Features (Basic Level + Auth)

### Authentication
- ✅ User Registration (email/password)
- ✅ User Login (JWT tokens)
- ✅ User Logout (clear token)
- ✅ Protected routes (frontend & backend)

### Todo Operations (per user)
- ✅ Add Task (user-specific)
- ✅ View Tasks (filtered by user_id)
- ✅ Update Task (own tasks only)
- ✅ Delete Task (own tasks only)
- ✅ Mark Complete/Incomplete

## Database Schema

### users (Better Auth managed)
```sql
id          TEXT PRIMARY KEY
email       TEXT UNIQUE NOT NULL
name        TEXT
created_at  TIMESTAMP DEFAULT NOW()
```

### tasks
```sql
id           SERIAL PRIMARY KEY
user_id      TEXT REFERENCES users(id)
title        VARCHAR(200) NOT NULL
description  TEXT
completed    BOOLEAN DEFAULT FALSE
created_at   TIMESTAMP DEFAULT NOW()
updated_at   TIMESTAMP DEFAULT NOW()
```

**Indexes**: tasks.user_id, tasks.completed

## API Endpoints

### Authentication (Better Auth)
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login user
- `POST /api/auth/signout` - Logout user

### Tasks (Protected)
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

All task endpoints require valid JWT token and validate user_id matches token.

## Security Requirements
- ✅ JWT token validation on all protected endpoints
- ✅ User data isolation (filter by user_id)
- ✅ Password hashing (Better Auth handles)
- ✅ HTTPS in production
- ✅ CORS configured for frontend domain
- ✅ SQL injection prevention (SQLModel ORM)
- ✅ XSS prevention (React escaping)
- ✅ No secrets in code (use .env)

## Development Workflow

### Initial Setup
```bash
# Install frontend dependencies
cd frontend && npm install

# Install backend dependencies
cd backend && uv sync

# Set up environment variables
cp .env.example .env
# Configure DATABASE_URL, JWT_SECRET, etc.
```

### Run Development Servers
```bash
# Frontend (http://localhost:3000)
cd frontend && npm run dev

# Backend (http://localhost:8000)
cd backend && uv run uvicorn app.main:app --reload
```

### Database Migrations
```bash
# Create migration
cd backend && alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Deployment Checklist

### Vercel (Frontend)
- [ ] Push to GitHub repository
- [ ] Connect repo to Vercel
- [ ] Set environment variables (NEXT_PUBLIC_API_URL, etc.)
- [ ] Deploy and verify

### Backend (Railway/Render)
- [ ] Configure DATABASE_URL (Neon connection string)
- [ ] Set JWT_SECRET and other secrets
- [ ] Deploy FastAPI app
- [ ] Run database migrations
- [ ] Test API endpoints

### Neon Database
- [ ] Create Neon project
- [ ] Copy connection string
- [ ] Run initial migrations
- [ ] Verify tables created

## Testing Strategy

### Frontend
```bash
# Run tests
npm test

# E2E tests
npm run test:e2e
```

### Backend
```bash
# Run tests
uv run pytest

# With coverage
uv run pytest --cov=app
```

### Manual Testing
1. Register new user
2. Login and verify JWT token stored
3. Create tasks (verify in database)
4. Update task title/description
5. Mark task complete/incomplete
6. Delete task
7. Logout and verify access denied
8. Test with multiple users (data isolation)

## Code Standards

### Frontend (TypeScript/React)
- Use TypeScript strict mode
- Functional components with hooks
- Server Components by default (use 'use client' when needed)
- Tailwind for styling (no inline styles)
- Clear component names (PascalCase)
- Extract reusable components

### Backend (Python/FastAPI)
- Type hints on all functions
- Pydantic models for validation
- SQLModel for database models
- Async endpoints where possible
- Structured error responses
- Proper HTTP status codes

## Common Issues & Solutions

### CORS Errors
Configure FastAPI CORS middleware:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourapp.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### JWT Token Validation
Backend must verify JWT from Better Auth:
```python
from jose import jwt

def verify_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
```

### Database Connection
Use connection pooling for Neon PostgreSQL:
```python
from sqlmodel import create_engine

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
```

## Success Criteria
- [ ] User can register and login
- [ ] JWT authentication working
- [ ] Tasks CRUD operations functional
- [ ] Multi-user data isolation verified
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed and accessible
- [ ] Database migrations applied
- [ ] All tests passing
- [ ] No console errors in browser
- [ ] API responds < 200ms for CRUD operations

## Related Agents
- `database.md` - Database operations and migrations
- `deployment.md` - Deployment workflows
- `testing.md` - Testing strategies

## Commands to Use
- `/sp.specify` - Update Phase II spec
- `/sp.plan` - Revise architecture plan
- `/sp.tasks` - Break down implementation tasks
- `/sp.implement` - Execute implementation
- `/sp.phr` - Create Prompt History Record
- `/sp.checklist` - Generate test checklist
- `/sp.git.commit_pr` - Commit and create PR

---

**Remember**: Phase II builds on Phase I foundation. Maintain stateless architecture for future phases (Kubernetes, cloud deployment).
