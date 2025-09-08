# Production-Ready Kubernetes GitOps Observability Project

## 🎯 Project Overview

This project combines multiple DevOps practices into a single comprehensive solution, implementing **GitOps workflows**, **complete observability stack**, **canary deployments**, and **incident management** on Kubernetes. It demonstrates production-grade deployment patterns using industry-standard tools.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ArgoCD        │    │  Istio Service  │    │   Monitoring    │
│   (GitOps)      │────▶  Mesh (Canary)  │────▶  Stack         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  GitHub Repo    │    │   Sample App    │    │   Grafana +     │
│  (Source)       │    │   (v1 + v2)     │    │   Prometheus    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  K8s Manifests  │    │  Incident       │    │   Jaeger        │
│  (YAML)         │    │  Tracker App    │    │   (Tracing)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
prod-k8s-gitops-observability/
├── README.md
├── manifests/
│   ├── base/                    # Base application deployment
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── canary/                  # Canary deployment with Istio
│   │   ├── deployment-v2.yaml
│   │   └── istio.yaml
│   ├── monitoring/              # Monitoring configurations
│   │   └── incident-tracker-servicemonitor.yaml
│   ├── tracing/                 # Jaeger tracing setup
│   ├── argocd/                  # ArgoCD Applications
│   │   └── incident-tracker-app.yaml
│   └── incident-tracker/        # Incident management app
│       ├── deployment.yaml
│       ├── service.yaml
│       └── virtual-service.yaml
├── incident-tracker/            # Flask application source
│   ├── app.py
│   ├── Dockerfile
│   └── templates/
│       └── index.html
├── helm-charts/                 # Helm configurations
├── ansible/                     # Automation scripts
├── dashboards/                  # Grafana dashboards
├── screenshots/                 # Demo screenshots
└── logs/                        # Application logs
```

## 🛠️ Technologies Used

### Core Infrastructure
- **Kubernetes**: Minikube for local development
- **Istio**: Service mesh for canary deployments
- **ArgoCD**: GitOps continuous deployment
- **Helm**: Package manager for Kubernetes

### Observability Stack
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards
- **Jaeger**: Distributed tracing
- **Loki**: Log aggregation (via Helm)

### Application Stack
- **Flask**: Python web framework for incident tracker
- **SQLite**: Lightweight database
- **Docker**: Containerization
- **Bootstrap**: Frontend styling

### Development Tools
- **Git**: Version control
- **GitHub**: Repository hosting
- **Docker Hub**: Container registry

## 🚀 Quick Start

### Prerequisites
- Docker installed
- Minikube installed
- kubectl configured
- Helm 3.x installed
- Git configured

### 1. Clone Repository
```bash
git clone https://github.com/Anagha-07/prod-k8s-gitops-observability.git
cd prod-k8s-gitops-observability
```

### 2. Start Minikube
```bash
minikube start --memory=2200mb --cpus=2
minikube addons enable ingress
minikube addons enable metrics-server
```

### 3. Install Istio
```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```

### 4. Deploy ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 5. Install Monitoring Stack
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update

kubectl create namespace monitoring
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring
helm install jaeger jaegertracing/jaeger -n monitoring
```

### 6. Deploy Applications
```bash
# Deploy base application
kubectl apply -f manifests/base/

# Deploy canary version
kubectl apply -f manifests/canary/

# Deploy incident tracker
kubectl apply -f manifests/incident-tracker/

# Setup ArgoCD application
kubectl apply -f manifests/argocd/incident-tracker-app.yaml
```

## 🔧 Access Applications

### Port Forwarding Commands
```bash
# ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Access: https://localhost:8080

# Grafana Dashboard
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
# Access: http://localhost:3000

# Jaeger UI
kubectl port-forward svc/jaeger-query -n monitoring 16686:16686
# Access: http://localhost:16686

# Sample Application
kubectl port-forward svc/sample-app 8888:80
# Access: http://localhost:8888

# Incident Tracker
kubectl port-forward svc/incident-tracker 5050:80
# Access: http://localhost:5050

# Prometheus
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090
# Access: http://localhost:9090
```

### Default Credentials
- **ArgoCD**: admin / (get password with: `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d`)
- **Grafana**: admin / prom-operator

## 📊 Key Features Implemented

### 1. GitOps Workflow
- ✅ ArgoCD automatically syncs from Git repository
- ✅ Declarative configuration management
- ✅ Self-healing deployments

### 2. Canary Deployments
- ✅ Istio-based traffic splitting (90% v1, 10% v2)
- ✅ Progressive rollout capability
- ✅ A/B testing support

### 3. Complete Observability
- ✅ Metrics collection with Prometheus
- ✅ Custom application metrics
- ✅ Distributed tracing with Jaeger
- ✅ Centralized logging with Loki
- ✅ Visual dashboards with Grafana

### 4. Incident Management
- ✅ Custom Flask application for incident tracking
- ✅ Kubernetes-native deployment
- ✅ Prometheus metrics integration
- ✅ Bootstrap-based responsive UI

### 5. Production Patterns
- ✅ Service mesh architecture
- ✅ Automated monitoring and alerting
- ✅ Container security best practices
- ✅ Resource optimization

## 🧪 Testing the Setup

### Test Canary Deployment
```bash
# Test traffic distribution
for i in {1..10}; do curl http://localhost:8888/; echo; done
```

### Test Incident Tracker
1. Navigate to http://localhost:5050
2. Add a new incident
3. Check metrics in Prometheus at http://localhost:9090
4. View custom dashboards in Grafana

### Test GitOps Flow
1. Modify any manifest in `manifests/` directory
2. Commit and push changes
3. Observe automatic sync in ArgoCD UI
4. Verify deployment updates in Kubernetes

## 📈 Monitoring & Alerts

### Custom Metrics
- `incident_created_total`: Counter for total incidents created
- Application performance metrics via Prometheus
- Kubernetes cluster metrics via kube-prometheus-stack

### Dashboards
- Kubernetes cluster overview
- Application performance metrics  
- Incident tracker custom metrics
- Jaeger trace visualization

## 🔄 CI/CD Integration

While not implemented in this version, the project is ready for GitHub Actions integration:

```yaml
# Example workflow structure
name: Deploy to K8s
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker image
      - name: Update manifests
      - name: ArgoCD auto-sync triggers deployment
```

## 🎯 Project Objectives Achieved

1. ✅ **GitOps Implementation**: ArgoCD manages deployments from Git
2. ✅ **Canary Deployments**: Istio enables traffic splitting
3. ✅ **Complete Observability**: Metrics, logs, and traces integrated
4. ✅ **Incident Management**: Custom Flask application deployed
5. ✅ **Production Readiness**: Best practices and monitoring implemented

## 🐛 Troubleshooting

### Common Issues
- **Resource constraints**: Ensure Minikube has adequate memory (2GB+)
- **Port conflicts**: Check if ports are already in use
- **ArgoCD sync issues**: Verify GitHub repository access
- **Metrics not appearing**: Check ServiceMonitor labels match Prometheus

### Debug Commands
```bash
# Check pod status
kubectl get pods --all-namespaces

# View logs
kubectl logs -f deployment/incident-tracker

# Check Istio sidecar injection
kubectl describe pod <pod-name>
```

## 🚧 Future Enhancements

- [ ] Automated testing pipeline with GitHub Actions
- [ ] Advanced alerting rules with Alertmanager
- [ ] Multi-environment deployments (dev/staging/prod)
- [ ] Security scanning integration
- [ ] Database migration management
- [ ] Performance benchmarking automation

## 📚 References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Istio Service Mesh](https://istio.io/latest/docs/)
- [Prometheus Monitoring](https://prometheus.io/docs/)
- [Grafana Dashboards](https://grafana.com/docs/)
