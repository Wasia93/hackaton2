# Phase IV: AI-Assisted Kubernetes Tools Setup

This guide covers setting up AI-powered tools for Kubernetes operations.

## Prerequisites

- Docker Desktop installed and running
- Minikube installed
- kubectl configured
- OpenAI API key (for kubectl-ai)

---

## 1. Gordon (Docker AI Assistant)

Gordon is Docker's built-in AI assistant.

### Setup
Gordon comes built into Docker Desktop 4.27+. No separate installation needed.

### Usage
```bash
# Ask Gordon for help
docker ai "how do I build a multi-stage Dockerfile?"

# Get container troubleshooting help
docker ai "why is my container crashing?"

# Generate docker-compose configurations
docker ai "create a docker-compose for a Python FastAPI app with PostgreSQL"
```

---

## 2. kubectl-ai

kubectl-ai translates natural language to kubectl commands.

### Installation

```bash
# Using brew (macOS/Linux)
brew install sozercan/kubectl-ai/kubectl-ai

# Using go install
go install github.com/sozercan/kubectl-ai@latest

# Or download binary from releases
# https://github.com/sozercan/kubectl-ai/releases
```

### Configuration

```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key"

# Or use Azure OpenAI
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_API_KEY="your-azure-key"
```

### Usage

```bash
# Scale deployment
kubectl-ai "scale the backend deployment to 5 replicas in todo-app namespace"

# Get pod logs
kubectl-ai "show me logs from the backend pod in todo-app namespace"

# Describe resources
kubectl-ai "describe the backend service in todo-app"

# Create resources
kubectl-ai "create a configmap named app-config with key1=value1"

# Debug issues
kubectl-ai "why are pods in todo-app namespace not running?"
```

---

## 3. kagent (Kubernetes AI Agent)

kagent provides intelligent Kubernetes diagnostics and operations.

### Installation

```bash
# Using pip
pip install kagent

# Or using pipx
pipx install kagent
```

### Configuration

```bash
# Set API key
export OPENAI_API_KEY="your-api-key"
```

### Usage

```bash
# Diagnose cluster issues
kagent diagnose

# Analyze specific namespace
kagent analyze -n todo-app

# Get recommendations
kagent recommend -n todo-app

# Interactive mode
kagent chat
```

### Example Session

```bash
$ kagent chat
> Why is my backend pod crashing?

kagent: Analyzing pod status in current namespace...
Found pod 'backend-xxx' in CrashLoopBackOff state.

Diagnosis:
- Container exit code: 1
- Last log: "Database connection refused"

Recommendations:
1. Check DATABASE_URL secret is correctly set
2. Verify database service is running
3. Check network policies allow database access

Would you like me to show the pod logs? (y/n)
```

---

## 4. Quick Start: Local Kubernetes Deployment

### Step 1: Start Minikube

```bash
# Start with sufficient resources
minikube start --driver=docker --cpus=4 --memory=8192

# Enable metrics server for HPA
minikube addons enable metrics-server
```

### Step 2: Build and Load Images

```bash
cd C:\hackathon2\hackaton2

# Build images
docker build -f docker/backend.Dockerfile -t todo-backend:latest .
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .

# Load into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Step 3: Deploy with Helm

```bash
# Create namespace and deploy
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  --set secrets.databaseUrl="your-database-url" \
  --set secrets.jwtSecret="your-jwt-secret" \
  --set secrets.geminiApiKey="your-gemini-key"

# Check status
kubectl get pods -n todo-app
```

### Step 4: Access Application

```bash
# Option 1: Port forward
kubectl port-forward svc/frontend 3000:3000 -n todo-app

# Option 2: Minikube service
minikube service frontend -n todo-app
```

### Step 5: Use AI Tools

```bash
# Check deployment with kubectl-ai
kubectl-ai "show all pods in todo-app namespace and their status"

# Diagnose issues with kagent
kagent analyze -n todo-app

# Scale with natural language
kubectl-ai "scale backend to 5 replicas in todo-app"
```

---

## 5. Troubleshooting with AI

### Common Issues

**Pods not starting:**
```bash
kubectl-ai "why are pods not starting in todo-app namespace?"
kagent diagnose -n todo-app
```

**Service not accessible:**
```bash
kubectl-ai "debug why frontend service is not accessible"
```

**High resource usage:**
```bash
kubectl-ai "show resource usage for all pods in todo-app"
kagent recommend -n todo-app
```

---

## 6. Useful Commands Reference

| Task | kubectl-ai Command |
|------|-------------------|
| List pods | "show all pods in todo-app" |
| View logs | "show logs from backend pod" |
| Scale | "scale backend to 3 replicas" |
| Restart | "restart the backend deployment" |
| Describe | "describe backend service" |
| Delete | "delete pod backend-xxx" |
| Port forward | "forward port 8000 from backend service" |

---

**Version**: 1.0.0
**Last Updated**: 2026-02-03
