# Skill: k8s.deploy

## Description
Deploy application to Kubernetes (Minikube or cloud)

## Usage
```
/k8s.deploy
/k8s.deploy --cloud=azure
/k8s.deploy --cloud=gke
```

## What It Does
- Builds Docker images
- Loads images to Kubernetes cluster
- Deploys using Helm chart
- Verifies deployment health

## Commands Executed

### Local (Minikube)
```bash
# Start Minikube
minikube start

# Build images
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
docker build -f docker/backend.Dockerfile -t todo-backend:latest .

# Load to Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Deploy with Helm
helm upgrade --install todo-app ./helm/todo-app -n todo-app --create-namespace

# Check status
kubectl get pods -n todo-app
```

### Cloud (Azure AKS / Google GKE)
```bash
# Push images to registry
docker tag todo-frontend:latest $REGISTRY/todo-frontend:latest
docker push $REGISTRY/todo-frontend:latest

# Deploy with Helm
helm upgrade --install todo-app ./helm/todo-app \
  --set frontend.image.repository=$REGISTRY/todo-frontend \
  --set frontend.image.tag=latest \
  -n todo-app --create-namespace
```

## Prerequisites

### Minikube
- Minikube installed and running
- Docker images built
- Helm installed
- kubectl configured

### Cloud Kubernetes
- AKS/GKE cluster created
- kubectl configured with cluster credentials
- Container registry configured
- Images pushed to registry

## Deployment Components
- **Namespace**: todo-app
- **Deployments**: frontend, backend, mcp-server
- **Services**: frontend-svc, backend-svc, mcp-svc
- **ConfigMaps**: app-config
- **Secrets**: todo-secrets (DATABASE_URL, JWT_SECRET, etc.)
- **Ingress**: todo-ingress (HTTPS)

## Create Secrets (First Time)
```bash
kubectl create namespace todo-app

kubectl create secret generic todo-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=jwt-secret=$JWT_SECRET \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  -n todo-app
```

## Verification Steps
```bash
# Check pod status
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check ingress
kubectl get ingress -n todo-app

# Check logs
kubectl logs -f deployment/backend -n todo-app

# Port-forward for local testing
kubectl port-forward svc/frontend 3000:3000 -n todo-app
```

## Flags
- `--cloud=azure` - Deploy to Azure AKS
- `--cloud=gke` - Deploy to Google GKE
- `--cloud=oke` - Deploy to Oracle OKE
- `--local` - Deploy to Minikube (default)
- `--dry-run` - Show what would be deployed without applying

## Post-Deployment Checks
- [ ] All pods in Running state
- [ ] Services have endpoints
- [ ] Ingress configured (if cloud)
- [ ] Health checks passing
- [ ] Logs showing no errors
- [ ] Application accessible

## Accessing Application

### Minikube
```bash
# Get service URL
minikube service frontend -n todo-app --url

# Or use port-forward
kubectl port-forward svc/frontend 3000:3000 -n todo-app
# Visit: http://localhost:3000
```

### Cloud
```bash
# Get ingress URL
kubectl get ingress -n todo-app
# Visit the EXTERNAL-IP or hostname
```

## Troubleshooting

### Pods Not Starting
```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### ImagePullBackOff
- Minikube: Load image with `minikube image load`
- Cloud: Verify image exists in registry
- Check imagePullSecrets configured

### CrashLoopBackOff
- Check environment variables in secrets
- Verify database connection
- Check health check configuration

## Rollback
```bash
# Helm rollback
helm rollback todo-app -n todo-app

# Or rollback specific deployment
kubectl rollout undo deployment/backend -n todo-app
```

## Clean Up
```bash
# Uninstall Helm release
helm uninstall todo-app -n todo-app

# Delete namespace
kubectl delete namespace todo-app
```

## Related Files
- `docker/` - Dockerfiles
- `helm/todo-app/` - Helm chart
- `k8s/` - Kubernetes manifests

## Related Agents
- `.claude/agents/phase4-kubernetes.md`
- `.claude/agents/deployment.md`

---

**Tip**: Use Minikube for local testing before deploying to cloud Kubernetes.
