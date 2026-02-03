# Phase IV: Kubernetes Deployment - Specification

**Feature**: Containerization and Local Kubernetes Deployment
**Phase**: Phase IV - Docker & Kubernetes
**Status**: Draft
**Created**: 2026-01-26
**Updated**: 2026-01-26

---

## 1. Overview

Containerize the Phase III full-stack application (Frontend, Backend, MCP Server) and deploy it to a local Kubernetes cluster using Minikube. This phase enables cloud-native architecture while maintaining local development capabilities.

### Purpose
- Containerize all services for consistent deployment
- Enable orchestration with Kubernetes
- Prepare infrastructure for cloud deployment (Phase V)
- Demonstrate DevOps best practices with Helm charts
- Enable AI-assisted operations with kubectl-ai and kagent

### Constraints
- **No manual coding** - All code generated via Claude Code using this spec
- **Spec-Driven Development** - Follow Specify -> Plan -> Tasks -> Implement
- **Local-first** - Minikube for local Kubernetes (no cloud yet)
- **Phase III compatibility** - All existing functionality must work
- **Stateless services** - All state in external database (Neon PostgreSQL)

### Key Changes from Phase III

| Aspect | Phase III | Phase IV |
|--------|-----------|----------|
| Deployment | Local processes | Docker containers |
| Orchestration | None | Kubernetes (Minikube) |
| Scaling | Manual | Horizontal Pod Autoscaler |
| Health Checks | Basic | Liveness/Readiness probes |
| Configuration | .env files | ConfigMaps & Secrets |
| Package Management | npm/pip | Helm charts |

---

## 2. User Journeys

### UJ-1: Developer Local Deployment
**As a developer**
**I want to** deploy the entire application locally with one command
**So that** I can test the full stack in a production-like environment

**Flow**:
1. Developer starts Minikube: `minikube start`
2. Developer builds Docker images: `docker-compose build`
3. Developer loads images to Minikube: `minikube image load`
4. Developer deploys with Helm: `helm install todo-app ./helm/todo-app`
5. All pods start and become ready
6. Developer accesses app via `minikube service frontend`

**Acceptance Criteria**:
- All 3 services (frontend, backend, mcp) containerized
- Single Helm command deploys entire stack
- All pods reach Running state within 2 minutes
- Application accessible via Minikube tunnel
- Existing Phase III features work unchanged

---

### UJ-2: Service Health Monitoring
**As an operator**
**I want to** monitor service health status
**So that** I can ensure application reliability

**Flow**:
1. Kubernetes runs liveness probes every 10 seconds
2. Kubernetes runs readiness probes every 5 seconds
3. If backend fails liveness probe, pod is restarted
4. If service fails readiness probe, traffic is diverted
5. Operator views pod status: `kubectl get pods -n todo-app`
6. Operator views logs: `kubectl logs -n todo-app deployment/backend`

**Acceptance Criteria**:
- Health endpoints return 200 OK when healthy
- Liveness probes restart unhealthy containers
- Readiness probes prevent traffic to unready pods
- Health status visible in kubectl output
- Automatic recovery from transient failures

---

### UJ-3: Configuration Management
**As a developer**
**I want to** configure services via Kubernetes resources
**So that** sensitive data is not hardcoded

**Flow**:
1. Create Kubernetes Secret with sensitive values (API keys, DB URL)
2. Create ConfigMap with non-sensitive configuration
3. Deploy services that reference these resources
4. Services read configuration from environment variables
5. Update Secret without rebuilding images

**Acceptance Criteria**:
- Database URL stored in Secret
- JWT secret stored in Secret
- OpenAI API key stored in Secret
- API URL stored in ConfigMap
- Services read config via env vars
- No secrets in Docker images or source code

---

### UJ-4: AI-Assisted Operations
**As an operator**
**I want to** use AI tools to manage Kubernetes
**So that** I can operate more efficiently

**Flow**:
1. Operator asks kubectl-ai: "scale backend to 5 replicas"
2. kubectl-ai translates to: `kubectl scale deployment backend --replicas=5`
3. Operator confirms and executes
4. Operator asks kagent: "diagnose why pod is crashing"
5. kagent analyzes logs and events
6. kagent provides diagnosis and suggested fix

**Acceptance Criteria**:
- kubectl-ai installed and configured
- kagent installed and configured
- Natural language commands work
- AI provides accurate suggestions
- Operations follow Kubernetes best practices

---

### UJ-5: Horizontal Scaling
**As an operator**
**I want to** scale services based on load
**So that** the application handles varying traffic

**Flow**:
1. HPA configured with CPU threshold (70%)
2. Load increases on backend service
3. HPA detects high CPU utilization
4. HPA scales backend from 2 to 4 replicas
5. Load balancer distributes traffic across pods
6. Load decreases, HPA scales down to minimum

**Acceptance Criteria**:
- HPA configured for backend service
- Minimum 2 replicas, maximum 10
- Scale up at 70% CPU utilization
- Scale down after sustained low usage
- Service remains available during scaling

---

## 3. Functional Requirements

### FR-1: Docker Containerization

**Priority**: CRITICAL
**Dependencies**: Phase III codebase

**Requirements**:
- Create optimized Dockerfiles for each service
- Use multi-stage builds to minimize image size
- Frontend: Node.js 20 Alpine base
- Backend: Python 3.13 Slim base
- Follow Docker security best practices
- Include .dockerignore files

**Dockerfiles to Create**:

1. **frontend.Dockerfile**
   - Multi-stage build (builder + production)
   - Install dependencies and build Next.js
   - Production image runs `npm start`
   - Expose port 3000

2. **backend.Dockerfile**
   - Python 3.13 slim base
   - Install UV and dependencies
   - Run FastAPI with Uvicorn
   - Expose port 8000

3. **mcp.Dockerfile** (if separate service)
   - Python 3.13 slim base
   - MCP server components only
   - Expose port 8001

---

### FR-2: Docker Compose for Local Development

**Priority**: HIGH
**Dependencies**: FR-1

**Requirements**:
- Single docker-compose.yml for all services
- Network configuration for inter-service communication
- Volume mounts for development (hot reload)
- Environment variable configuration
- Health check definitions

**Services**:
- `frontend`: Next.js application
- `backend`: FastAPI application
- `mcp`: MCP Server (can be combined with backend)

---

### FR-3: Kubernetes Manifests

**Priority**: CRITICAL
**Dependencies**: FR-1

**Requirements**:
- Create namespace `todo-app`
- Deployment manifests for all services
- Service manifests for internal networking
- ConfigMap for non-sensitive configuration
- Secret for sensitive configuration
- Ingress for external access (optional for local)

**Manifests to Create**:

1. **namespace.yaml**
   - Namespace: `todo-app`

2. **secrets.yaml**
   - Database URL
   - JWT secret
   - OpenAI API key

3. **configmap.yaml**
   - Backend URL
   - Frontend settings
   - Environment-specific config

4. **frontend/deployment.yaml**
   - 2 replicas
   - Liveness/readiness probes
   - Resource limits

5. **frontend/service.yaml**
   - ClusterIP or LoadBalancer
   - Port 3000

6. **backend/deployment.yaml**
   - 3 replicas
   - Liveness/readiness probes
   - Environment from secrets/configmap
   - Resource limits

7. **backend/service.yaml**
   - ClusterIP
   - Port 8000

8. **mcp/deployment.yaml** (if separate)
   - 2 replicas
   - Liveness/readiness probes

9. **mcp/service.yaml** (if separate)
   - ClusterIP
   - Port 8001

---

### FR-4: Health Check Endpoints

**Priority**: CRITICAL
**Dependencies**: Phase III backend

**Requirements**:
- `/health` endpoint on all services
- Returns JSON with status and timestamp
- Checks critical dependencies (database connection)
- Fast response time (< 100ms)

**Health Endpoint Spec**:
```json
GET /health
Response 200:
{
  "status": "healthy",
  "service": "backend",
  "timestamp": "2026-01-26T10:00:00Z",
  "checks": {
    "database": "ok"
  }
}

Response 503:
{
  "status": "unhealthy",
  "service": "backend",
  "timestamp": "2026-01-26T10:00:00Z",
  "checks": {
    "database": "failed"
  }
}
```

---

### FR-5: Helm Chart

**Priority**: HIGH
**Dependencies**: FR-3

**Requirements**:
- Helm chart for entire application
- Parameterized values.yaml
- Templates for all Kubernetes resources
- Support for different environments
- Documentation in Chart.yaml

**Helm Structure**:
```
helm/todo-app/
  Chart.yaml       # Chart metadata
  values.yaml      # Default configuration
  templates/
    namespace.yaml
    secrets.yaml
    configmap.yaml
    frontend/
      deployment.yaml
      service.yaml
    backend/
      deployment.yaml
      service.yaml
      hpa.yaml
    mcp/
      deployment.yaml
      service.yaml
```

**values.yaml Parameters**:
- `frontend.replicaCount`
- `frontend.image.repository`
- `frontend.image.tag`
- `backend.replicaCount`
- `backend.image.repository`
- `backend.image.tag`
- `database.url` (reference to secret)
- `secrets.jwtSecret`
- `secrets.openaiApiKey`

---

### FR-6: Horizontal Pod Autoscaler

**Priority**: MEDIUM
**Dependencies**: FR-3

**Requirements**:
- HPA for backend service
- Scale based on CPU utilization
- Minimum 2 replicas
- Maximum 10 replicas
- Target CPU: 70%

---

### FR-7: Resource Management

**Priority**: MEDIUM
**Dependencies**: FR-3

**Requirements**:
- Define resource requests and limits
- Prevent resource starvation
- Enable fair scheduling

**Resource Spec**:
```yaml
Frontend:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"

Backend:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

---

## 4. Non-Functional Requirements

### NFR-1: Performance
- Container startup time < 30 seconds
- Health check response < 100ms
- No performance regression from Phase III
- Image size < 500MB each

### NFR-2: Security
- No secrets in Docker images
- Non-root container users
- Read-only file systems where possible
- Network policies for pod isolation

### NFR-3: Reliability
- Automatic pod restart on failure
- Rolling updates with zero downtime
- Graceful shutdown (SIGTERM handling)
- State persistence in external database

### NFR-4: Operability
- Clear pod and container naming
- Structured logging to stdout
- Health endpoints for monitoring
- kubectl-ai and kagent integration

### NFR-5: Portability
- Works on Windows, macOS, Linux
- Minikube-compatible
- Ready for cloud Kubernetes (Phase V)

---

## 5. Acceptance Criteria

### AC-1: Docker Images
- Frontend image builds successfully
- Backend image builds successfully
- MCP image builds successfully (or combined with backend)
- Images run locally with docker-compose
- All Phase III functionality works in containers

### AC-2: Kubernetes Deployment
- All manifests apply without errors
- All pods reach Running state
- Services accessible via port-forward
- Services accessible via Minikube tunnel
- No CrashLoopBackOff errors

### AC-3: Health Checks
- `/health` endpoint returns 200 OK
- Liveness probes configured correctly
- Readiness probes configured correctly
- Unhealthy containers are restarted

### AC-4: Configuration
- Secrets stored in Kubernetes Secrets
- ConfigMaps used for non-sensitive config
- Environment variables injected correctly
- No hardcoded secrets in images

### AC-5: Helm Chart
- Helm chart installs successfully
- Helm chart upgrades work
- Values can be overridden
- Helm uninstall removes all resources

### AC-6: AI Operations
- kubectl-ai responds to natural language
- kagent provides diagnostic information
- Operations follow best practices

### AC-7: Scaling
- HPA configured correctly
- Pods scale up under load
- Pods scale down when idle
- Service remains available during scaling

---

## 6. Out of Scope (Phase IV)

The following features are explicitly **excluded** from Phase IV:

- Cloud deployment (Azure, GCP, Oracle) - Phase V
- Kafka event streaming - Phase V
- Dapr integration - Phase V
- CI/CD pipelines - Phase V
- Production TLS certificates
- External DNS configuration
- Persistent volume claims (database is external)
- Service mesh (Istio, Linkerd)
- Monitoring stack (Prometheus, Grafana) - optional stretch goal
- Multi-cluster deployment

---

## 7. Dependencies

### Tools Required
- **Docker Desktop** or Docker Engine
- **Minikube** - Local Kubernetes cluster
- **kubectl** - Kubernetes CLI
- **Helm 3** - Package manager
- **kubectl-ai** - AI-powered kubectl (optional but recommended)
- **kagent** - Kubernetes AI agent (optional but recommended)

### External Services
- **Neon PostgreSQL** - Database (existing from Phase II/III)
- **OpenAI API** - For chatbot (existing from Phase III)

### Phase III Prerequisites
- Backend API functional
- Frontend application functional
- MCP server functional
- Authentication working
- Database schema in place

---

## 8. Risks and Mitigations

### Risks
- **R-1**: Minikube resource constraints (mitigated by proper resource limits)
- **R-2**: Image pull issues in Minikube (mitigated by local image loading)
- **R-3**: Network configuration complexity (mitigated by clear service definitions)
- **R-4**: Configuration drift between dev and k8s (mitigated by Helm values)
- **R-5**: kubectl-ai/kagent availability (mitigated by manual fallback)

### Assumptions
- **A-1**: Docker Desktop or Docker Engine available
- **A-2**: Minikube can allocate 4GB RAM, 2 CPUs
- **A-3**: External Neon database accessible from local network
- **A-4**: Developer has basic Kubernetes familiarity
- **A-5**: Phase III codebase is stable

---

## 9. Success Metrics

Phase IV is successful when:
- All 3 services containerized and running in Docker
- Docker Compose deployment works locally
- Kubernetes deployment works in Minikube
- All pods Running with healthy probes
- Helm chart installs/upgrades/uninstalls cleanly
- kubectl-ai and kagent operational (if available)
- All Phase III features work unchanged
- HPA scales pods correctly
- No manual coding (spec-driven only)

---

## 10. Project Structure

```
hackaton2/
  docker/
    frontend.Dockerfile
    backend.Dockerfile
    mcp.Dockerfile (optional)
    docker-compose.yml
    .dockerignore
  k8s/
    namespace.yaml
    secrets.yaml
    configmap.yaml
    frontend/
      deployment.yaml
      service.yaml
    backend/
      deployment.yaml
      service.yaml
      hpa.yaml
    mcp/
      deployment.yaml
      service.yaml
  helm/
    todo-app/
      Chart.yaml
      values.yaml
      templates/
        namespace.yaml
        secrets.yaml
        configmap.yaml
        frontend/
          deployment.yaml
          service.yaml
        backend/
          deployment.yaml
          service.yaml
          hpa.yaml
        mcp/
          deployment.yaml
          service.yaml
  frontend/     # Existing Phase III
  phase2/
    backend/    # Existing Phase III
  specs/
    phase4-kubernetes/
      spec.md       # This file
      plan.md       # Architecture (to be created)
      tasks.md      # Task breakdown (to be created)
```

---

## 11. References

- [Phase III Spec](../phase3-ai-chatbot/spec.md) - AI Chatbot requirements
- [Phase II Spec](../phase2-web-app/spec.md) - Web app foundation
- [Constitution](../../.specify/memory/constitution.md) - Project principles
- [AGENTS.md](../../AGENTS.md) - Agent workflow instructions
- [Phase IV Agent](../../.claude/agents/phase4-kubernetes.md) - Kubernetes agent guide
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

---

**Spec Version**: 1.0.0
**Approved By**: [Pending approval]
**Approval Date**: [Pending]
**Next Step**: Create plan.md (HOW to build)
