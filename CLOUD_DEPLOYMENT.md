# Cloud Deployment Guide

Phase V: Advanced Cloud Deployment with Kubernetes and Kafka

---

## Overview

This guide covers deploying the Todo application to production-grade Kubernetes on cloud providers with Kafka/Redpanda event streaming.

## Prerequisites

- Docker Desktop or Docker Engine
- kubectl CLI
- Helm 3.x
- Cloud provider CLI (az, gcloud, or oci)
- Domain name (for TLS)

---

## 1. Local Validation (Minikube)

Before deploying to cloud, validate everything works locally.

### Start Minikube

```bash
# Start with sufficient resources
minikube start --driver=docker --cpus=4 --memory=8192

# Enable required addons
minikube addons enable metrics-server
minikube addons enable ingress
```

### Build and Load Images

```bash
cd C:\hackathon2\hackaton2

# Build images
docker build -f docker/backend.Dockerfile -t todo-backend:latest .
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .

# Load into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Deploy with Helm

```bash
# Deploy application
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  --set secrets.databaseUrl="your-neon-database-url" \
  --set secrets.jwtSecret="your-jwt-secret" \
  --set secrets.geminiApiKey="your-gemini-api-key"

# Check status
kubectl get pods -n todo-app
kubectl get svc -n todo-app
```

### Access Application

```bash
# Port forward
kubectl port-forward svc/frontend 3000:3000 -n todo-app

# Or use Minikube service
minikube service frontend -n todo-app
```

---

## 2. Cloud Kubernetes Setup

### Option A: Azure AKS

```bash
# Login to Azure
az login

# Create resource group
az group create --name todo-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group todo-rg \
  --name todo-aks \
  --node-count 3 \
  --node-vm-size Standard_B2s \
  --enable-managed-identity \
  --generate-ssh-keys \
  --enable-cluster-autoscaler \
  --min-count 2 \
  --max-count 10

# Get credentials
az aks get-credentials --resource-group todo-rg --name todo-aks

# Verify connection
kubectl get nodes
```

### Option B: Google GKE

```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Create GKE cluster
gcloud container clusters create todo-gke \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-medium \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 10

# Get credentials
gcloud container clusters get-credentials todo-gke --zone us-central1-a

# Verify connection
kubectl get nodes
```

### Option C: Oracle OKE

```bash
# Configure OCI CLI
oci setup config

# Create cluster via Console or CLI
# See: https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengcreatingclusterusingoke.htm

# Get kubeconfig
oci ce cluster create-kubeconfig \
  --cluster-id <cluster-ocid> \
  --file ~/.kube/config
```

---

## 3. Install Prerequisites

### NGINX Ingress Controller

```bash
# Add Helm repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

### cert-manager (for TLS)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.0/cert-manager.yaml

# Wait for it to be ready
kubectl wait --for=condition=Available deployment --all -n cert-manager --timeout=300s

# Create ClusterIssuer (edit email first!)
kubectl apply -f k8s/cluster-issuer.yaml
```

---

## 4. Deploy Redpanda (Kafka)

### Option 1: Redpanda in Kubernetes

```bash
# Add Redpanda Helm repo
helm repo add redpanda https://charts.redpanda.com
helm repo update

# Install Redpanda
helm install redpanda redpanda/redpanda \
  --namespace todo-app \
  --create-namespace \
  -f kafka/redpanda-values.yaml

# Wait for pods
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/name=redpanda -n todo-app --timeout=300s

# Create topics
kubectl apply -f kafka/kafka-topics.yaml
```

### Option 2: Redpanda Cloud (Managed)

1. Create account at https://cloud.redpanda.com
2. Create a Serverless cluster
3. Get bootstrap servers URL
4. Create topics via Console
5. Use connection details in Helm values

---

## 5. Deploy Application

### Push Images to Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag and push
docker tag todo-backend:latest ghcr.io/wasia93/hackaton2/backend:latest
docker tag todo-frontend:latest ghcr.io/wasia93/hackaton2/frontend:latest

docker push ghcr.io/wasia93/hackaton2/backend:latest
docker push ghcr.io/wasia93/hackaton2/frontend:latest
```

### Deploy with Helm

```bash
# Create namespace
kubectl create namespace todo-app

# Deploy with production values
helm upgrade --install todo-app ./helm/todo-app \
  --namespace todo-app \
  -f helm/todo-app/values-production.yaml \
  --set secrets.databaseUrl="postgresql://user:pass@host/db" \
  --set secrets.jwtSecret="your-production-jwt-secret" \
  --set secrets.geminiApiKey="your-gemini-api-key" \
  --set ingress.hosts[0].host="todo.yourdomain.com" \
  --set ingress.tls[0].hosts[0]="todo.yourdomain.com"

# Check deployment
kubectl get pods -n todo-app
kubectl get ingress -n todo-app
```

### Configure DNS

Point your domain to the Ingress controller's external IP:

```bash
# Get external IP
kubectl get svc ingress-nginx-controller -n ingress-nginx

# Create DNS A record:
# todo.yourdomain.com -> <EXTERNAL-IP>
```

---

## 6. Enable Kafka Events

Update the backend deployment to enable Kafka:

```bash
helm upgrade todo-app ./helm/todo-app \
  --namespace todo-app \
  -f helm/todo-app/values-production.yaml \
  --set kafka.enabled=true \
  --set kafka.bootstrapServers="redpanda.todo-app.svc.cluster.local:9092" \
  --reuse-values
```

---

## 7. Verify Deployment

### Check All Pods Running

```bash
kubectl get pods -n todo-app
# All should be Running/Ready
```

### Check Ingress

```bash
kubectl get ingress -n todo-app
# Should show ADDRESS with external IP
```

### Check TLS Certificate

```bash
kubectl get certificate -n todo-app
# Should show READY=True
```

### Test Application

```bash
# Health check
curl https://todo.yourdomain.com/health

# Should return:
# {"status":"healthy","service":"Todo API",...}
```

### Check Kafka Events

```bash
# Connect to Redpanda pod
kubectl exec -it redpanda-0 -n todo-app -- rpk topic consume task-events --num 5
```

---

## 8. Monitoring

### View Logs

```bash
# Backend logs
kubectl logs -l app=backend -n todo-app -f

# Frontend logs
kubectl logs -l app=frontend -n todo-app -f
```

### Check HPA

```bash
kubectl get hpa -n todo-app
```

### Resource Usage

```bash
kubectl top pods -n todo-app
```

---

## 9. Troubleshooting

### Pods Not Starting

```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Ingress Not Working

```bash
kubectl describe ingress -n todo-app
kubectl logs -l app.kubernetes.io/name=ingress-nginx -n ingress-nginx
```

### Certificate Issues

```bash
kubectl describe certificate -n todo-app
kubectl logs -l app=cert-manager -n cert-manager
```

### Database Connection Failed

- Verify DATABASE_URL secret is correct
- Check if Neon allows connections from cluster IP
- Test connection from a pod:
  ```bash
  kubectl run psql-test --rm -it --image=postgres:15 -- psql "your-database-url"
  ```

---

## 10. Cleanup

### Delete Application

```bash
helm uninstall todo-app -n todo-app
```

### Delete Redpanda

```bash
helm uninstall redpanda -n todo-app
```

### Delete Cluster

```bash
# AKS
az aks delete --resource-group todo-rg --name todo-aks

# GKE
gcloud container clusters delete todo-gke --zone us-central1-a

# Delete resource group (AKS)
az group delete --name todo-rg
```

---

## CI/CD Integration

The GitHub Actions workflows automatically:

1. **On Pull Request**: Run tests, build images
2. **On Push to Main**: Build, push to registry, deploy to cluster

### Required Secrets

Set these in GitHub repository settings:

- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - JWT signing secret
- `GEMINI_API_KEY` - Google Gemini API key
- `KUBE_CONFIG` - Base64 encoded kubeconfig file

```bash
# Encode kubeconfig
cat ~/.kube/config | base64 -w 0
```

---

**Version**: 1.0.0
**Last Updated**: 2026-02-03
