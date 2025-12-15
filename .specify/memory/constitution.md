# Evolution of Todo - Project Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**No code is written without an approved specification.**

* Every feature requires: Spec (WHAT) → Plan (HOW) → Tasks (BREAKDOWN) → Implement
* Specifications must include user journeys, acceptance criteria, and constraints
* Claude Code is the executor; humans are the architects
* All code changes must reference Task IDs from `specs/<feature>/tasks.md`
* Constraint: Refine specs until Claude Code generates correct output—no manual coding allowed

### II. Progressive Evolution Architecture

**The system evolves through 5 distinct phases, each building on the previous.**

* Phase I: In-memory Python console app (foundation)
* Phase II: Full-stack web app with persistent storage
* Phase III: AI-powered chatbot with MCP tools
* Phase IV: Containerized Kubernetes deployment
* Phase V: Cloud-native event-driven system

Each phase must maintain backward compatibility with core features. Architecture decisions must consider future phases.

### III. Stateless-First Design

**All services must be stateless; state persists only in the database.**

* No in-memory sessions or caching that cannot be reconstructed
* Database (Neon PostgreSQL) is the single source of truth
* Enables horizontal scaling and cloud-native deployment
* Conversation state, tasks, and user data all persist to database
* Server restarts must not lose any user data or context

### IV. AI-Native Architecture

**The application is designed for AI agent interaction, not just human UIs.**

* MCP (Model Context Protocol) server exposes all operations as tools
* Natural language commands map to structured API calls
* Stateless chat endpoint persists conversation to database
* AI agents (OpenAI Agents SDK) orchestrate MCP tool calls
* Human and AI interfaces share the same backend API

### V. Security-First Authentication

**Multi-user system with proper authentication and data isolation.**

* Better Auth for user authentication (signup/signin)
* JWT tokens for API authorization
* Every API endpoint validates user identity
* Data filtered by user_id—users only see their own tasks
* Shared secret between frontend (Better Auth) and backend (FastAPI)
* No task can be accessed or modified without valid JWT token

### VI. Cloud-Native from Day One

**Design for containerization, orchestration, and distributed systems.**

* Docker containers for all services
* Kubernetes-ready architecture (Helm charts)
* Event-driven communication via Kafka
* Dapr for distributed application runtime (Pub/Sub, State, Bindings)
* Environment-based configuration (no hardcoded secrets)
* Observability: structured logging, metrics, health checks

### VII. Minimal Viable Complexity

**Start simple, add complexity only when required by the phase.**

* Phase I: Simple Python with in-memory lists
* Phase II: Add database, web frontend
* Phase III: Add AI chatbot, MCP server
* Phase IV: Add Docker, Kubernetes
* Phase V: Add Kafka, Dapr, cloud deployment

Do not over-engineer early phases. Each phase adds one new dimension of complexity.

---

## Technology Stack Constraints

### Phase I: Console App
* **Language**: Python 3.13+
* **Package Manager**: UV
* **Storage**: In-memory (Python data structures)
* **Interface**: Command-line interface

### Phase II: Full-Stack Web App
* **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
* **Backend**: Python FastAPI, SQLModel ORM
* **Database**: Neon Serverless PostgreSQL
* **Auth**: Better Auth with JWT tokens
* **Hosting**: Vercel (frontend), any cloud (backend)

### Phase III: AI Chatbot
* **Chatbot UI**: OpenAI ChatKit
* **AI Framework**: OpenAI Agents SDK
* **MCP Server**: Official MCP SDK (Python)
* **Tools**: MCP tools for task CRUD operations
* **Architecture**: Stateless chat endpoint + database persistence

### Phase IV: Local Kubernetes
* **Containerization**: Docker, Docker Compose
* **Orchestration**: Minikube (local Kubernetes)
* **Package Manager**: Helm charts
* **AIOps**: kubectl-ai, kagent, Docker AI (Gordon)

### Phase V: Cloud Deployment
* **Cloud**: Azure AKS / Google GKE / Oracle OKE
* **Event Streaming**: Kafka (self-hosted via Strimzi or Redpanda Cloud)
* **Runtime**: Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation)
* **CI/CD**: GitHub Actions
* **Monitoring**: Kubernetes-native observability

---

## Development Workflow

### Spec-Driven Workflow (Mandatory)
1. **Write Specification** (`/sp.specify`) - Define WHAT to build
2. **Create Plan** (`/sp.plan`) - Define HOW to build it
3. **Break into Tasks** (`/sp.tasks`) - Define atomic, testable work units
4. **Implement via Claude Code** (`/sp.implement`) - Generate code from tasks
5. **Review & Iterate** - Refine specs if Claude Code output is incorrect

### Testing Requirements
* Unit tests for business logic (Python: pytest, TypeScript: Jest/Vitest)
* Integration tests for API endpoints
* End-to-end tests for critical user journeys
* Tests written before implementation (TDD where practical)

### Git Workflow
* Feature branches for each phase (`phase-1-console`, `phase-2-web`, etc.)
* Commit messages reference Task IDs
* Pull requests include spec references
* Use `/sp.git.commit_pr` for spec-driven commits

### Documentation Requirements
* `README.md` - Setup instructions for each phase
* `CLAUDE.md` - References AGENTS.md (single source of truth)
* `specs/<feature>/` - Spec, plan, tasks for each feature
* `.specify/memory/constitution.md` - This file (project principles)
* `history/prompts/` - Prompt History Records (PHR)
* `history/adr/` - Architectural Decision Records

---

## API Design Principles

### RESTful Conventions
* `GET /api/{user_id}/tasks` - List tasks
* `POST /api/{user_id}/tasks` - Create task
* `GET /api/{user_id}/tasks/{id}` - Get task
* `PUT /api/{user_id}/tasks/{id}` - Update task
* `DELETE /api/{user_id}/tasks/{id}` - Delete task
* `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Error Handling
* Use HTTP status codes correctly (200, 201, 400, 401, 404, 500)
* Return JSON error responses with `{"error": "message", "detail": {...}}`
* Log errors with structured logging (timestamp, user_id, error type)

### Data Validation
* Validate all inputs (Pydantic models in FastAPI)
* Title: required, 1-200 characters
* Description: optional, max 1000 characters
* User isolation: all queries filter by authenticated user_id

---

## Database Schema Principles

### Core Tables

**users** (managed by Better Auth)
* `id` (string, primary key)
* `email` (string, unique)
* `name` (string)
* `created_at` (timestamp)

**tasks**
* `id` (integer, primary key, auto-increment)
* `user_id` (string, foreign key → users.id)
* `title` (string, not null, max 200 chars)
* `description` (text, nullable, max 1000 chars)
* `completed` (boolean, default false)
* `priority` (string, optional: "high", "medium", "low") - Phase II+
* `due_date` (datetime, nullable) - Phase V
* `created_at` (timestamp, default now)
* `updated_at` (timestamp, auto-update)

**conversations** (Phase III+)
* `id` (integer, primary key)
* `user_id` (string, foreign key → users.id)
* `created_at` (timestamp)
* `updated_at` (timestamp)

**messages** (Phase III+)
* `id` (integer, primary key)
* `conversation_id` (integer, foreign key → conversations.id)
* `user_id` (string, foreign key → users.id)
* `role` (string: "user" | "assistant")
* `content` (text)
* `created_at` (timestamp)

### Indexes
* `tasks.user_id` (for filtering by user)
* `tasks.completed` (for status filtering)
* `messages.conversation_id` (for fetching conversation history)

---

## MCP Tools Specification (Phase III+)

All task operations must be exposed as MCP tools:

* `add_task` - Create new task (user_id, title, description)
* `list_tasks` - Retrieve tasks (user_id, status filter)
* `complete_task` - Mark task complete (user_id, task_id)
* `delete_task` - Remove task (user_id, task_id)
* `update_task` - Modify task (user_id, task_id, title, description)

MCP tools are stateless and interact with database directly.

---

## Event-Driven Architecture (Phase V)

### Kafka Topics
* `task-events` - All task CRUD operations
* `reminders` - Scheduled reminder triggers
* `task-updates` - Real-time client synchronization

### Event Schema
All events include:
* `event_type` (string: "created", "updated", "completed", "deleted")
* `task_id` (integer)
* `user_id` (string)
* `timestamp` (datetime ISO 8601)
* `task_data` (object with full task details)

### Dapr Components
* **Pub/Sub**: `pubsub.kafka` (Kafka abstraction)
* **State Management**: `state.postgresql` (conversation state)
* **Bindings**: Dapr Jobs API for scheduled reminders
* **Secrets**: `secretstores.kubernetes` (API keys, DB credentials)

---

## Security Requirements

* **Authentication**: Better Auth (email/password, social login optional)
* **Authorization**: JWT tokens with 7-day expiration
* **Data Isolation**: All queries filter by authenticated user_id
* **Secrets Management**: Environment variables, never in code
* **HTTPS**: Required in production (TLS/SSL)
* **CORS**: Configured for frontend domain only
* **SQL Injection**: Prevented by SQLModel ORM (parameterized queries)
* **XSS**: Prevented by React/Next.js escaping

---

## Performance Standards

* API response time: < 200ms p95 for CRUD operations
* Database queries: Use indexes, avoid N+1 queries
* Frontend: Server-side rendering (SSR) for initial load
* Chatbot: Response within 3 seconds (LLM latency included)
* Kubernetes: Auto-scaling based on CPU/memory thresholds

---

## Observability & Monitoring

* **Logging**: Structured JSON logs (timestamp, level, user_id, message)
* **Metrics**: Request count, latency, error rate (Prometheus format)
* **Health Checks**: `/health` endpoint on all services
* **Kubernetes**: Liveness and readiness probes
* **Tracing**: Distributed tracing for multi-service requests (optional Phase V)

---

## Governance

* **Constitution Supremacy**: This file supersedes all other practices
* **Amendment Process**: Requires spec update, approval, and ADR documentation
* **Compliance**: All PRs must verify adherence to these principles
* **Spec-Kit Tools**: All development follows SpecKit Plus workflow
* **Human as Tool**: Agents must request clarification when uncertain
* **No Improvisation**: If spec is unclear, stop and ask—never guess

---

**Version**: 1.0.0
**Ratified**: 2025-12-15
**Last Amended**: 2025-12-15
**Project**: Evolution of Todo - Hackathon II
