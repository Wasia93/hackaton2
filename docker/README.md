# Phase IV: Docker & Kubernetes Deployment Guide

**Task**: T-028
**From**: specs/phase4-kubernetes/spec.md, specs/phase4-kubernetes/plan.md

This guide covers deploying the Evolution of Todo application using Docker and Kubernetes.

---

## Prerequisites

### Required Tools

1. **Docker Desktop** or Docker Engine
   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. **Minikube** (for local Kubernetes)
   ```bash
   # Windows (with Chocolatey)
   choco install minikube

   # macOS
   brew install minikube

   # Linux
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```

3. **kubectl** (Kubernetes CLI)
   ```bash
   # Windows (with Chocolatey)
   choco install kubernetes-cli

   # macOS
   brew install kubectl

   # Linux
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

4. **Helm 3** (Kubernetes package manager)
   ```bash
   # Windows (with Chocolatey)
   choco install kubernetes-helm

   # macOS
   brew install helm

   # Linux
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

### Environment Variables

Create a `.env` file in the `docker/` directory with the following variables:

```bash
# Copy from template
cp docker/.env.example docker/.env

# Edit with your values
# DATABASE_URL - Your Neon PostgreSQL connection string
# JWT_SECRET - A secure random string (min 32 chars)
# OPENAI_API_KEY - Your OpenAI API key
```

---

## Option 1: Docker Compose (Local Development)

### Build and Run

```bash
# Navigate to project root
cd hackaton2

# Build images
docker-compose -f docker/docker-compose.yml build

# Run services
docker-compose -f docker/docker-compose.yml up

# Run in background
docker-compose -f docker/docker-compose.yml up -d
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Stop Services

```bash
docker-compose -f docker/docker-compose.yml down
```

---

## Option 2: Kubernetes with kubectl (Raw Manifests)

### 1. Start Minikube

```bash
# Start with recommended resources
minikube start --driver=docker --cpus=4 --memory=8192

# Verify cluster is running
kubectl cluster-info
```

### 2. Build Docker Images

```bash
# Build images
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
docker build -f docker/backend.Dockerfile -t todo-backend:latest .
```

### 3. Load Images to Minikube

```bash
# Load images into Minikube's Docker daemon
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Verify images are loaded
minikube image ls | grep todo
```

### 4. Configure Secrets

Edit `k8s/secrets.yaml` with your actual values:

```yaml
stringData:
  database-url: "postgresql://your-user:your-pass@your-host.neon.tech/your-db?sslmode=require"
  jwt-secret: "your-jwt-secret-minimum-32-characters"
  openai-api-key: "sk-your-openai-api-key"
```

### 5. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (edit first!)
kubectl apply -f k8s/secrets.yaml

# Create configmap
kubectl apply -f k8s/configmap.yaml

# Deploy frontend
kubectl apply -f k8s/frontend/

# Deploy backend
kubectl apply -f k8s/backend/
```

### 6. Verify Deployment

```bash
# Check pods status
kubectl get pods -n todo-app

# Wait for all pods to be Running
kubectl wait --for=condition=ready pod -l app=frontend -n todo-app --timeout=120s
kubectl wait --for=condition=ready pod -l app=backend -n todo-app --timeout=120s

# Check services
kubectl get svc -n todo-app
```

### 7. Access the Application

```bash
# Option A: Port forwarding
kubectl port-forward svc/frontend 3000:3000 -n todo-app

# Option B: Minikube service (opens browser)
minikube service frontend -n todo-app

# Option C: Minikube tunnel (for LoadBalancer services)
minikube tunnel
```

---

## Option 3: Kubernetes with Helm

### 1. Start Minikube (if not running)

```bash
minikube start --driver=docker --cpus=4 --memory=8192
```

### 2. Build and Load Images

```bash
# Build images
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
docker build -f docker/backend.Dockerfile -t todo-backend:latest .

# Load to Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 3. Install with Helm

```bash
# Install chart with secrets
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  --set secrets.databaseUrl="postgresql://user:pass@host.neon.tech/db?sslmode=require" \
  --set secrets.jwtSecret="your-jwt-secret-minimum-32-characters" \
  --set secrets.openaiApiKey="sk-your-openai-api-key"
```

### 4. Verify Installation

```bash
# Check Helm release
helm list -n todo-app

# Check pods
kubectl get pods -n todo-app

# Check all resources
kubectl get all -n todo-app
```

### 5. Access the Application

```bash
minikube service frontend -n todo-app
```

### 6. Upgrade Configuration

```bash
# Change replica count
helm upgrade todo-app ./helm/todo-app \
  -n todo-app \
  --set backend.replicaCount=5

# View changes
kubectl get pods -n todo-app
```

### 7. Uninstall

```bash
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
```

---

## Troubleshooting

### Pod Won't Start (ImagePullBackOff)

```bash
# Check if images are loaded in Minikube
minikube image ls | grep todo

# Reload images if needed
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### Pod Crashing (CrashLoopBackOff)

```bash
# Check pod logs
kubectl logs -l app=backend -n todo-app

# Check pod events
kubectl describe pod -l app=backend -n todo-app
```

### Health Check Failing

```bash
# Test health endpoint manually
kubectl exec -it deployment/backend -n todo-app -- curl http://localhost:8000/health

# Check environment variables
kubectl exec -it deployment/backend -n todo-app -- env | grep DATABASE
```

### Service Not Accessible

```bash
# Verify service exists
kubectl get svc -n todo-app

# Check endpoints
kubectl get endpoints -n todo-app

# Test internal connectivity
kubectl run -it --rm debug --image=busybox -n todo-app -- wget -qO- http://backend:8000/health
```

### Minikube Issues

```bash
# Reset Minikube
minikube delete
minikube start --driver=docker --cpus=4 --memory=8192

# View Minikube dashboard
minikube dashboard
```

---

## Useful Commands

### View Logs

```bash
# All backend logs
kubectl logs -l app=backend -n todo-app --tail=100

# Follow logs in real-time
kubectl logs -f deployment/backend -n todo-app
```

### Scale Services

```bash
# Scale manually
kubectl scale deployment backend --replicas=5 -n todo-app

# Check HPA status
kubectl get hpa -n todo-app
```

### Execute Commands in Container

```bash
# Open shell in backend container
kubectl exec -it deployment/backend -n todo-app -- /bin/bash

# Run one-off command
kubectl exec deployment/backend -n todo-app -- python -c "print('hello')"
```

### View Resource Usage

```bash
# Pod resource usage (requires metrics-server)
minikube addons enable metrics-server
kubectl top pods -n todo-app
```

---

## AI-Assisted Operations (Optional)

### kubectl-ai

```bash
# Install kubectl-ai
# https://github.com/sozercan/kubectl-ai

# Example usage
kubectl-ai "scale backend to 5 replicas in todo-app namespace"
kubectl-ai "show me pods that are not ready"
```

### kagent

```bash
# Install kagent
# https://github.com/kagent-ai/kagent

# Example usage
kagent "diagnose why backend pods are crashing"
kagent "check application health in todo-app namespace"
```

---

## Directory Structure

```
hackaton2/
  docker/
    frontend.Dockerfile    # Multi-stage Next.js build
    backend.Dockerfile     # Python FastAPI build
    docker-compose.yml     # Local development
    .dockerignore          # Files to exclude from build
    .env.example           # Environment template
    README.md              # This file
  k8s/
    namespace.yaml         # Kubernetes namespace
    secrets.yaml           # Sensitive configuration
    configmap.yaml         # Non-sensitive configuration
    frontend/
      deployment.yaml      # Frontend pods
      service.yaml         # Frontend service
    backend/
      deployment.yaml      # Backend pods
      service.yaml         # Backend service
      hpa.yaml            # Autoscaling
  helm/
    todo-app/
      Chart.yaml           # Helm chart metadata
      values.yaml          # Default configuration
      templates/           # Kubernetes templates
```

---

## Next Steps

- **Phase V**: Cloud deployment with Azure AKS, GCP GKE, or Oracle OKE
- **CI/CD**: GitHub Actions for automated builds and deployments
- **Monitoring**: Prometheus and Grafana for observability
