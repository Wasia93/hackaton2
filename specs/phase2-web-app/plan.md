# Phase II: Todo Web Application - Technical Plan

**Feature**: Full-Stack Multi-User Todo Web Application
**Phase**: Phase II - Web Application  
**Status**: Ready for Implementation
**Created**: 2025-12-15
**Updated**: 2025-12-15

**References**:
- [Specification](./spec.md) - WHAT to build
- [Phase I Plan](../phase1-console-app/plan.md) - Foundation architecture
- [Constitution](../../.specify/memory/constitution.md) - Project principles

---

## 1. Architecture Overview

### 1.1 System Architecture

\`\`\`
┌──────────────────────────────────────────────────────────────────┐
│                   Phase II: Full-Stack Web Application            │
│                                                                   │
│  ┌────────────────────┐          ┌──────────────────────┐        │
│  │   Frontend (Next.js│          │  Backend (FastAPI)   │        │
│  │   + Better Auth)   │◄────────►│  + SQLModel + JWT    │        │
│  │   Vercel           │  HTTPS   │  Railway/Render      │        │
│  └────────────────────┘          └──────────┬───────────┘        │
│                                              │                    │
│                                              ▼                    │
│                                  ┌──────────────────────┐        │
│                                  │  Neon PostgreSQL      │        │
│                                  │  (Serverless)         │        │
│                                  └──────────────────────┘        │
└──────────────────────────────────────────────────────────────────┘
\`\`\`

### 1.2 Monorepo Structure

\`\`\`
hackaton2/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # DB connection
│   │   ├── models/            # SQLModel models
│   │   ├── routers/           # API endpoints
│   │   └── middleware/        # Auth middleware
│   ├── alembic/               # Migrations
│   └── requirements.txt       # Python deps
├── frontend/                   # Next.js frontend
│   ├── app/                   # App Router pages
│   ├── components/            # React components
│   ├── lib/                   # Utilities
│   └── package.json           # Node deps
└── specs/phase2-web-app/      # This plan
\`\`\`

---

## 2. Technology Stack

### Frontend
- **Next.js 16+** - App Router, React 19+
- **TypeScript 5+** - Type safety
- **Tailwind CSS** - Styling
- **Better Auth** - Authentication
- **Fetch API** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **SQLModel** - ORM
- **Alembic** - Migrations
- **PyJWT** - JWT verification
- **Neon PostgreSQL** - Database

---

## 3. Database Schema

### Users Table (Better Auth managed)
\`\`\`sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
\`\`\`

### Tasks Table
\`\`\`sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_user_id (user_id),
    INDEX idx_completed (completed)
);
\`\`\`

---

## 4. Authentication Flow

### Better Auth (Frontend)
- Email/password authentication
- JWT token generation
- httpOnly cookie storage
- Shared secret with backend

### FastAPI Middleware (Backend)
- JWT verification using PyJWT
- Extract user_id from token
- Attach user to request context
- Reject unauthenticated requests

### JWT Token Structure
\`\`\`json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890
}
\`\`\`

---

## 5. REST API Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/auth/signup | No | Register |
| POST | /api/auth/login | No | Login |
| GET | /api/{user_id}/tasks | Yes | List tasks |
| POST | /api/{user_id}/tasks | Yes | Create task |
| PUT | /api/{user_id}/tasks/{id} | Yes | Update task |
| DELETE | /api/{user_id}/tasks/{id} | Yes | Delete task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Yes | Toggle |

---

## 6. Frontend Architecture

### Pages
- **/** - Landing page
- **/auth/signup** - Registration
- **/auth/login** - Login  
- **/dashboard** - Protected task list

### Components
- **TaskCard** - Single task display
- **TaskForm** - Create/edit form
- **AuthForm** - Login/signup
- **Header** - App header with logout
- **ProtectedRoute** - Auth guard

---

## 7. Implementation Order

### Phase 1: Backend Foundation (Tasks 1-15)
1. Setup backend structure
2. Database models
3. Migrations
4. Auth middleware
5. API endpoints

### Phase 2: Frontend Foundation (Tasks 16-25)  
1. Setup Next.js
2. Better Auth config
3. Layout & routing
4. UI components

### Phase 3: Integration (Tasks 26-35)
1. Connect frontend to API
2. Auth flow
3. CRUD operations

### Phase 4: Polish (Tasks 36-40)
1. Error handling
2. Loading states  
3. Responsive design
4. Deployment

---

**Plan Version**: 1.0.0
**Status**: Ready for Implementation
**Next**: Create tasks.md (atomic task breakdown)
