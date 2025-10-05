# Parte 3 – CI/CD y Monitorización

## Objetivo
Automatizar la construcción y despliegue de la app con un pipeline (Jenkins) y habilitar una monitorización básica del clúster.

## Plan
1. CI: construir y publicar imagen Docker en Docker Hub.
2. CD: actualizar Deployment de Kubernetes a la última imagen.
3. Monitorización básica: metrics-server (y opcional Prometheus/Grafana).

## Estructura
- Jenkinsfile (en la raíz del repo)
- parte2/deploy.sh (script de despliegue local)
- parte3/README.md (este archivo)

## Próximos pasos
- Levantar Jenkins en Docker.
- Crear credenciales en Jenkins (dockerhub y kubeconfig).
- Ejecutar el pipeline y validar el despliegue.

