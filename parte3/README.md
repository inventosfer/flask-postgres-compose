# Parte 3 – CI/CD y Monitorización

## Objetivo
Automatizar la construcción y despliegue de la aplicación mediante un pipeline CI/CD (Jenkins) y habilitar un sistema completo de monitorización en Kubernetes utilizando Prometheus y Grafana.

---

## Plan de trabajo

### CI/CD
- Jenkins construye la imagen Docker de la app Flask + Postgres.  
- La imagen se publica automáticamente en Docker Hub.  
- Jenkins ejecuta el script de despliegue (`deploy.sh`) para actualizar el Deployment de Kubernetes a la nueva versión.

### Monitorización
- **Prometheus** recopila métricas de:
  - Componentes de Kubernetes (`kubelet`, `cAdvisor`, `kube-state-metrics`).
  - Métricas del sistema (CPU, RAM, disco, red) mediante **Node Exporter**.
- **Grafana** visualiza las métricas con dashboards listos para usar:
  - Kubernetes Cluster (Prometheus)
  - Node Exporter Full Dashboard

---

## Estructura del proyecto

```bash

parte3/
├── prometheus-deploy.yaml # Servicio, deployment y configuración (ConfigMap)
├── grafana-deploy.yaml # Servicio y deployment de Grafana
├── node-exporter.yaml # DaemonSet y Service para Node Exporter
├── kube-state-metrics.yaml # (opcional) métricas de estado del clúster
├── Jenkinsfile # Pipeline de CI/CD
├── deploy.sh # Script de despliegue continuo
└── README.md # Este archivo

```



---


## Despliegue de la monitorización

Ejecutar todo el despliegue paso a paso en un solo bloque:

```bash
# 1. Crear namespace y desplegar Prometheus
kubectl create ns monitoring
kubectl apply -f parte3/prometheus-deploy.yaml

# 2. Desplegar Grafana
kubectl apply -f parte3/grafana-deploy.yaml

# 3. Desplegar Node Exporter (métricas del sistema)
kubectl apply -f parte3/node-exporter.yaml

# 4. (Opcional) Desplegar kube-state-metrics
kubectl apply -f parte3/kube-state-metrics.yaml

# 5. Verificar que todos los pods estén corriendo
kubectl -n monitoring get pods

# 6. Acceso rápido
# Prometheus:
#   minikube service -n monitoring prometheus --url
# Grafana (credenciales por defecto: admin / admin):
minikube service -n monitoring grafana --url

```

---

## Validacion rapida (Prueba de stress)


kubectl run stress-test --image=alpine:latest --restart=Never -- \
  sh -c "apk add --no-cache stress-ng && stress-ng --cpu 2 --vm 1 --vm-bytes 256M --timeout 60s"
kubectl delete pod stress-test

