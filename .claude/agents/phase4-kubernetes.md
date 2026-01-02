# Phase IV Kubernetes Deployment Agent

## Purpose
Expert agent for containerizing and deploying the application to local Kubernetes with Minikube (Phase IV).

## Responsibilities
- Create Docker containers for all services
- Write Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- Develop Helm charts for package management
- Set up Minikube for local Kubernetes cluster
- Implement health checks and readiness probes
- Use kubectl-ai and kagent for AI-assisted operations

## Technology Stack

### Containerization
- **Docker**: Container images
- **Docker Compose**: Local multi-service orchestration

### Orchestration
- **Minikube**: Local Kubernetes cluster
- **Helm**: Kubernetes package manager
- **kubectl**: Kubernetes CLI
- **kubectl-ai**: AI-powered kubectl assistant
- **kagent**: Kubernetes AI agent

### Services to Containerize
1. **Frontend** (Next.js)
2. **Backend** (FastAPI)
3. **MCP Server** (Python)
4. **Database** (PostgreSQL - or use external Neon)

## Project Structure
```
├── docker/
│   ├── frontend.Dockerfile
│   ├── backend.Dockerfile
│   ├── mcp.Dockerfile
│   └── docker-compose.yml
├── k8s/
│   ├── frontend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   ├── mcp/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── secrets.yaml
│   └── namespace.yaml
├── helm/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── frontend/
│           ├── backend/
│           └── mcp/
└── specs/phase4-kubernetes/  # Specifications (to be created)
```

## Docker Images

### Frontend Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./
RUN npm install --production
EXPOSE 3000
CMD ["npm", "start"]
```

### Backend Dockerfile
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock ./
RUN pip install uv && uv sync
COPY backend/ ./
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### MCP Server Dockerfile
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock ./
RUN pip install uv && uv sync
COPY backend/app/mcp/ ./app/mcp/
EXPOSE 8001
CMD ["uv", "run", "python", "-m", "app.mcp.server"]
```

## Kubernetes Manifests

### Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
```

### Frontend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://backend:8000"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Backend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: jwt-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: todo-app
spec:
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: ClusterIP
```

### Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
  namespace: todo-app
type: Opaque
stringData:
  database-url: postgresql://user:pass@neon.tech/db
  jwt-secret: your-secret-key
  openai-api-key: sk-...
```

## Helm Chart Structure

### Chart.yaml
```yaml
apiVersion: v2
name: todo-app
description: Evolution of Todo - Full Stack Application
version: 1.0.0
appVersion: "1.0.0"
```

### values.yaml
```yaml
frontend:
  replicaCount: 2
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 3000

backend:
  replicaCount: 3
  image:
    repository: todo-backend
    tag: latest
  service:
    port: 8000

mcp:
  replicaCount: 2
  image:
    repository: todo-mcp
    tag: latest
  service:
    port: 8001

database:
  external: true
  url: "postgresql://..."

secrets:
  jwtSecret: ""
  openaiApiKey: ""
```

## Development Workflow

### Build Docker Images
```bash
# Build all images
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
docker build -f docker/backend.Dockerfile -t todo-backend:latest .
docker build -f docker/mcp.Dockerfile -t todo-mcp:latest .
```

### Test with Docker Compose
```bash
docker-compose -f docker/docker-compose.yml up
```

### Start Minikube
```bash
minikube start --driver=docker --cpus=4 --memory=8192
```

### Load Images to Minikube
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
minikube image load todo-mcp:latest
```

### Deploy with kubectl
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/backend/
kubectl apply -f k8s/mcp/
```

### Deploy with Helm
```bash
# Install chart
helm install todo-app ./helm/todo-app -n todo-app --create-namespace

# Upgrade
helm upgrade todo-app ./helm/todo-app -n todo-app

# Uninstall
helm uninstall todo-app -n todo-app
```

## kubectl-ai and kagent Usage

### kubectl-ai Examples
```bash
# AI-powered kubectl assistance
kubectl-ai "scale backend to 5 replicas"
kubectl-ai "show me pods that are not ready"
kubectl-ai "restart frontend deployment"
```

### kagent Examples
```bash
# Kubernetes AI agent
kagent "diagnose why backend pods are crashing"
kagent "optimize resource usage"
kagent "check application health"
```

## Monitoring and Debugging

### Check Pod Status
```bash
kubectl get pods -n todo-app
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Port Forwarding (for local access)
```bash
kubectl port-forward svc/frontend 3000:3000 -n todo-app
kubectl port-forward svc/backend 8000:8000 -n todo-app
```

### Access via Minikube
```bash
minikube service frontend -n todo-app
minikube service backend -n todo-app
```

## Health Checks

### Liveness Probe
Checks if container is alive. Kubernetes restarts if fails.
- Frontend: `GET /`
- Backend: `GET /health`
- MCP: `GET /health`

### Readiness Probe
Checks if container is ready to serve traffic.
- Same endpoints as liveness
- Don't send traffic if not ready

### Health Endpoint Example
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

## Resource Management

### Resource Requests/Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Horizontal Pod Autoscaler (HPA)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Success Criteria
- [ ] All services containerized with Docker
- [ ] Docker Compose runs locally
- [ ] Minikube cluster running
- [ ] All pods in Running state
- [ ] Health checks passing
- [ ] Services accessible via port-forward or Minikube tunnel
- [ ] Helm chart deploys successfully
- [ ] kubectl-ai and kagent working
- [ ] Logs accessible for debugging
- [ ] Resources properly configured
- [ ] Auto-scaling configured

## Common Issues & Solutions

### ImagePullBackOff
- Load images to Minikube: `minikube image load <image>`
- Use `imagePullPolicy: IfNotPresent`

### CrashLoopBackOff
- Check logs: `kubectl logs <pod>`
- Verify environment variables and secrets
- Check health check configuration

### Service Not Accessible
- Verify service selector matches pod labels
- Use port-forward for testing
- Check Minikube tunnel: `minikube tunnel`

## Related Agents
- `deployment.md` - General deployment strategies
- `testing.md` - Testing in Kubernetes
- `phase5-cloud.md` - Next phase (cloud deployment)

## Commands to Use
- `/sp.specify` - Create Phase IV spec
- `/sp.plan` - Design Kubernetes architecture
- `/sp.tasks` - Break down containerization tasks
- `/sp.implement` - Execute implementation
- `/sp.phr` - Create Prompt History Record
- `/sp.adr` - Document K8s architecture decisions

---

**Remember**: Phase IV containerizes the app for cloud deployment. Keep stateless architecture and prepare for Phase V event-driven patterns.
