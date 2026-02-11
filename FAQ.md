# Frequently Asked Questions (FAQ)

## Evolution of Todo - Hackathon II

---

### Q1: What is this project about?

This is a progressive todo application that evolves across 6 phases — from a simple Python console app to a cloud-native, AI-powered platform deployed on both Vercel (serverless) and Azure AKS (Kubernetes). It demonstrates full-stack development, AI integration, containerization, and cloud deployment using Spec-Driven Development (SDD).

---

### Q2: What technologies are used in this project?

| Category | Technologies |
|----------|-------------|
| **Backend** | Python 3.12, FastAPI, SQLModel, Alembic, Uvicorn |
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS |
| **Database** | PostgreSQL (Neon serverless), SQLite (local dev) |
| **Authentication** | JWT (python-jose), bcrypt (passlib) |
| **AI Chatbot** | OpenAI GPT-4o-mini, MCP (Model Context Protocol) |
| **Containerization** | Docker (multi-stage builds), Docker Compose |
| **Orchestration** | Kubernetes, Helm 3, HPA, RBAC, Network Policies |
| **Cloud (Serverless)** | Vercel (frontend + backend serverless functions) |
| **Cloud (Kubernetes)** | Azure AKS, Azure Container Registry (ACR) |
| **CI/CD** | GitHub Actions (CI + CD pipelines) |
| **Event Streaming** | Apache Kafka (aiokafka), Dapr |
| **Monitoring** | Prometheus, Grafana |

---

### Q3: How is the frontend deployed on Vercel?

The Next.js 16 frontend is deployed as a Vercel project linked to the GitHub repository. Vercel automatically detects it as a Next.js app and builds it as serverless functions.

**Key steps:**
1. Vercel project is linked to the `hackaton2` GitHub repo
2. `NEXT_PUBLIC_API_URL` is set as an environment variable pointing to the backend URL (`https://backend-navy-five-43.vercel.app`)
3. Since `NEXT_PUBLIC_` variables are baked in at **build time**, the frontend must be redeployed after changing the API URL
4. Vercel auto-deploys on every push to the `main` branch

**Live URL:** https://hackaton2-omega.vercel.app

---

### Q4: How is the backend deployed on Vercel?

The FastAPI backend is deployed as a Vercel serverless Python function. This required creating an entry point file that Vercel recognizes.

**Key files:**
- `phase2/backend/api/index.py` — Entry point that imports the FastAPI app
- `phase2/backend/vercel.json` — Configuration for routing and function settings

**vercel.json structure:**
```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 60
    }
  },
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/index"
    }
  ]
}
```

**Environment variables set on Vercel:**
- `DATABASE_URL` — Neon PostgreSQL connection string
- `JWT_SECRET` — Secret key for JWT signing
- `JWT_ALGORITHM` — `HS256`
- `OPENAI_API_KEY` — OpenAI API key for chatbot
- `CORS_ORIGINS` — Allowed frontend origins
- `PROJECT_NAME` — App display name

**Live URL:** https://backend-navy-five-43.vercel.app

---

### Q5: How is the app deployed on Azure AKS?

The app runs on a 2-node Azure Kubernetes Service (AKS) cluster with Docker images stored in Azure Container Registry (ACR).

**Architecture:**
- **AKS Cluster:** `todo-aks` in West US 2, 2 nodes (Standard_B2s_v2)
- **Container Registry:** `todoacrhackathon.azurecr.io`
- **Namespace:** `todo-app`
- **Backend:** 2 replicas with HPA (auto-scales 2-10 pods at 70% CPU)
- **Frontend:** 2 replicas with LoadBalancer service
- **Services:** LoadBalancer (external IPs for both frontend and backend)

**Docker images are built with:**
```bash
docker build -f docker/backend.Dockerfile -t todoacrhackathon.azurecr.io/todo-backend:latest .
docker build -f docker/frontend.Dockerfile --build-arg NEXT_PUBLIC_API_URL=http://20.69.114.112 -t todoacrhackathon.azurecr.io/todo-frontend:latest .
```

**Key Kubernetes resources:**
- ConfigMap (`todo-config`) — Backend URL, model name, project name
- Secrets (`todo-secrets`) — Database URL, JWT secret, API keys
- Deployments with liveness/readiness probes on `/health`
- RBAC (service accounts, roles, role bindings)
- Network Policies (default deny + selective allow)

**Live URLs:**
- Frontend: http://20.42.153.18
- Backend: http://20.69.114.112

---

### Q6: How does the AI chatbot work?

The chatbot uses OpenAI's GPT-4o-mini model with function calling (tool use) to manage tasks through natural language.

**Flow:**
1. User sends a message via `POST /api/chat`
2. The message is sent to OpenAI with system instructions and 7 available tools
3. If GPT decides to call a tool (e.g., `create_task`), the backend executes it via MCP
4. The tool result is sent back to GPT for a final human-readable response
5. Both the user message and assistant response are saved to the database

**7 MCP Tools:**
| Tool | Description |
|------|-------------|
| `create_task` | Create a new task with title and optional description |
| `list_tasks` | Get all tasks for the authenticated user |
| `get_task` | Get a specific task by ID |
| `update_task` | Update task title or description |
| `complete_task` | Toggle task completion status |
| `delete_task` | Permanently delete a task |
| `search_tasks` | Search tasks by keyword |

**Security:** The `user_id` is automatically injected from the JWT token into every tool call, ensuring users can only access their own tasks.

---

### Q7: What is MCP (Model Context Protocol)?

MCP is a protocol that allows AI models to interact with external tools and data sources in a standardized way. In this project, MCP defines 7 tools (in OpenAI function calling format) that the AI agent can use to perform CRUD operations on tasks.

The `MCPServer` class in `app/mcp_server.py` registers all tools and handles execution. Each tool receives arguments from the AI model and executes the corresponding database operation.

---

### Q8: How does authentication work?

The app uses **JWT (JSON Web Token)** authentication:

1. **Registration:** User submits email + password. Password is hashed with bcrypt and stored in PostgreSQL.
2. **Login:** User submits credentials. If valid, a JWT token is returned containing the `user_id` in the `sub` claim.
3. **Protected Routes:** The JWT token is sent in the `Authorization: Bearer <token>` header. The backend verifies the token and extracts the `user_id`.
4. **Data Isolation:** Every database query filters by `user_id`, ensuring users can only access their own tasks.

**Token Configuration:**
- Algorithm: `HS256`
- Expiration: 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Libraries: `python-jose` for JWT, `passlib[bcrypt]` for password hashing

---

### Q9: What database is used and why?

**Production:** Neon PostgreSQL (serverless) — a serverless Postgres service that scales to zero and auto-scales on demand. Both Vercel and Azure deployments connect to the same Neon database in East US 2.

**Local Development:** SQLite — simple file-based database that requires no setup.

**ORM:** SQLModel — combines SQLAlchemy (database operations) with Pydantic (data validation) in a single library. Database migrations are handled by Alembic.

---

### Q10: What is the difference between the Vercel and Azure deployments?

| Aspect | Vercel | Azure AKS |
|--------|--------|-----------|
| **Type** | Serverless functions | Kubernetes containers |
| **Scaling** | Auto (managed by Vercel) | HPA (2-10 pods at 70% CPU) |
| **Cold starts** | Yes (serverless) | No (pods always running) |
| **Function timeout** | 10s (free) / 60s (pro) | No limit |
| **Cost** | Free tier available | Pay per node (~$30/mo for 2 nodes) |
| **SSL/HTTPS** | Automatic | Manual (LoadBalancer + cert-manager) |
| **Deployment** | `git push` auto-deploy | Docker build + ACR push + Helm upgrade |
| **Infrastructure** | Fully managed | Full control over K8s resources |

Both deployments connect to the same Neon PostgreSQL database and use the same OpenAI API key.

---

### Q11: How does the CI/CD pipeline work?

**CI Pipeline (`ci.yaml`)** — Runs on every push/PR to `main`:
1. **Backend Tests:** Installs Python dependencies, runs `pytest` with SQLite test database
2. **Frontend Build:** Installs Node dependencies, runs TypeScript check, builds Next.js
3. **Docker Build:** Builds both Dockerfiles (without pushing) to verify they compile
4. **Helm Lint:** Validates the Helm chart templates

**CD Pipeline (`deploy.yaml`)** — Runs on push to `main` or version tags:
1. Builds and pushes Docker images to GitHub Container Registry (GHCR)
2. Deploys to Kubernetes via `helm upgrade --install` with production values
3. Verifies rollout with `kubectl rollout status`

---

### Q12: What is Spec-Driven Development (SDD)?

SDD is the development methodology used throughout this project. It follows a structured workflow:

1. **Specify (WHAT)** — Define requirements, acceptance criteria, and constraints in `spec.md`
2. **Plan (HOW)** — Create technical architecture and design decisions in `plan.md`
3. **Tasks (BREAKDOWN)** — Break down into atomic, testable work units in `tasks.md`
4. **Implement (CODE)** — Generate code via Claude Code following the specs
5. **Review** — Refine and iterate

All specifications are stored in `specs/` with separate directories for each phase. Architectural decisions are documented in ADRs (Architecture Decision Records) in `history/adr/`.

---

### Q13: How does rate limiting work?

The backend has a custom `RateLimitMiddleware` that limits API requests:

- **General endpoints:** 100 requests per minute per IP
- **Auth endpoints** (`/auth/*`): 20 requests per minute per IP

This prevents abuse and brute-force login attempts. The middleware tracks requests in-memory using IP addresses and time windows.

---

### Q14: What Kubernetes resources are used?

| Resource | Purpose |
|----------|---------|
| **Namespace** (`todo-app`) | Isolates all app resources |
| **Deployments** | Backend (2 replicas) + Frontend (2 replicas) |
| **Services** | LoadBalancer for external access |
| **HPA** | Auto-scales backend from 2 to 10 pods at 70% CPU |
| **ConfigMap** | Non-sensitive config (backend URL, model name) |
| **Secrets** | Sensitive data (DB URL, JWT secret, API keys) |
| **RBAC** | Service accounts, roles, and role bindings |
| **Network Policies** | Default deny + selective allow between services |
| **Health Probes** | Liveness (every 10s) and readiness (every 5s) on `/health` |

---

### Q15: How does the event streaming (Kafka) work?

The app publishes task events to Apache Kafka for analytics:

**Events Published:**
- `task.created` — When a user creates a task
- `task.updated` — When a task is modified
- `task.completed` — When a task is toggled complete
- `task.deleted` — When a task is removed

**Architecture:**
- **Producer** (`event_service.py`): Publishes events asynchronously using `aiokafka`
- **Consumer** (`event_consumer.py`): Processes events for analytics (counts by type/user)
- **Topics:** `task-events`, `task-analytics`, `task-events-dlq` (dead letter queue)
- **Integration:** Dapr pub/sub component wraps Kafka for easier service-to-service messaging

Kafka is optional and controlled by `KAFKA_ENABLED=true/false` environment variable.

---

### Q16: What challenges were faced during deployment?

1. **CORS Issues:** Frontend and backend on different domains required proper CORS configuration with explicit origin URLs.

2. **`NEXT_PUBLIC_` env vars baked at build time:** Changing the API URL required rebuilding and redeploying the frontend, not just restarting pods.

3. **Vercel 10-second timeout:** The free plan limits serverless functions to 10 seconds. Gemini API calls exceeded this, so we switched to OpenAI GPT-4o-mini which responds faster.

4. **Trailing newlines in env vars:** Using `echo` to set Vercel environment variables added `\n` characters, breaking JWT algorithm detection (`HS256\n` instead of `HS256`). Fixed by using `printf` instead.

5. **ACR access lost:** The Azure Container Registry was deleted and had to be recreated, then re-attached to the AKS cluster.

6. **Docker image caching:** AKS pods used cached Docker images. Rebuilding with the correct `NEXT_PUBLIC_API_URL` and pushing to ACR was required to fix the frontend.

---

### Q17: What are the API endpoints?

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login, get JWT token | No |
| POST | `/tasks/` | Create task | Yes |
| GET | `/tasks/` | List user's tasks | Yes |
| GET | `/tasks/{id}` | Get specific task | Yes |
| PUT | `/tasks/{id}` | Update task | Yes |
| PATCH | `/tasks/{id}/toggle` | Toggle completion | Yes |
| DELETE | `/tasks/{id}` | Delete task | Yes |
| POST | `/api/chat` | Send message to AI chatbot | Yes |
| GET | `/api/chat/health` | Chat service health check | No |
| GET | `/health` | Backend health check | No |
| GET | `/analytics` | Kafka event analytics | No |
| GET | `/docs` | Swagger API documentation | No |

---

### Q18: How is the project structured?

```
hackaton2/
├── phase1/                        # Phase I: Console App
│   └── src/                       # Python CLI application
├── phase2/backend/                # Phase II-VI: FastAPI Backend
│   ├── api/index.py               # Vercel serverless entry point
│   ├── vercel.json                # Vercel configuration
│   └── app/
│       ├── api/                   # REST endpoints (auth, tasks, chat)
│       ├── core/                  # Config, database, auth, rate limiting
│       ├── models/                # SQLModel models
│       ├── services/              # Business logic, AI agent, events
│       └── mcp_tools/             # MCP tool implementations
├── frontend/                      # Next.js 16 Frontend
│   ├── app/                       # Pages (login, register, dashboard)
│   ├── components/                # UI components (TaskList, Chatbot)
│   └── services/                  # API clients
├── docker/                        # Dockerfiles + docker-compose
├── k8s/                           # Kubernetes manifests
├── helm/todo-app/                 # Helm chart
├── kafka/                         # Kafka configuration
├── .github/workflows/             # CI/CD pipelines
└── specs/                         # SDD specifications (per phase)
```

---

### Q19: What are the live deployment URLs?

**Vercel (Serverless):**
| Service | URL |
|---------|-----|
| Frontend | https://hackaton2-omega.vercel.app |
| Backend API | https://backend-navy-five-43.vercel.app |
| API Docs | https://backend-navy-five-43.vercel.app/docs |
| Health Check | https://backend-navy-five-43.vercel.app/health |

**Azure AKS (Kubernetes):**
| Service | URL |
|---------|-----|
| Frontend | http://20.42.153.18 |
| Backend API | http://20.69.114.112 |
| Health Check | http://20.69.114.112/health |

---

### Q20: How can I run the project locally?

**Option 1: Docker Compose (Easiest)**
```bash
cd docker
docker-compose up --build
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

**Option 2: Manual Setup**
```bash
# Backend
cd phase2/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install && npm run dev
```

**Required environment variables:**
```
DATABASE_URL=sqlite:///./todo.db
JWT_SECRET=your-secret-key-min-32-chars
OPENAI_API_KEY=your-openai-api-key
```
