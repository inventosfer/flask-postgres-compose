# Proyecto DevOps – CI/CD con Jenkins, Docker y Kubernetes (Minikube)

Este proyecto implementa un flujo CI/CD completo con **Jenkins**, **Docker Hub** y **Kubernetes (Minikube)** para desplegar automáticamente una aplicación **Flask + Postgres**.

El pipeline:
1. Clona el repositorio desde GitHub  
2. Construye y publica la imagen en Docker Hub  
3. Despliega la nueva versión en Kubernetes  
4. Realiza una prueba automática (`/ping`) para validar el despliegue  

---

## Versiones utilizadas
- Docker 28.5.0  
- kubectl 1.34.1  
- Minikube 1.37.0  
- Git 2.43.0  
- Jenkins LTS  
- Python 3.12 (Flask)

---

## Pipeline (Jenkinsfile)
```groovy
pipeline {
  agent any
  options { timestamps() }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build & Push Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            set -e
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            IMAGE="$DOCKER_USER/flask-postgres-compose"
            docker build -t "$IMAGE:latest" parte1
            docker push "$IMAGE:latest"
          '''
        }
      }
    }
    stage('Kube Deploy') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh '''
            export KUBECONFIG="$KUBECONFIG"
            kubectl -n parte2 set image deploy/flask-api flask-api="$DOCKER_USER/flask-postgres-compose:latest" --record=true
            kubectl -n parte2 rollout status deploy/flask-api --timeout=300s
            URL=$(minikube service -n parte2 flask-api --url | tail -n1)
            curl -fsS "$URL/ping" | grep -q '"status":"ok"'
          '''
        }
      }
    }
  }
}


---

## Resultado final

Comprobación final de la aplicación desplegada:

```bash
curl -fsS http://192.168.58.2:30476/ping
```

**Respuesta:**
```json
{"status":"ok"}
```


---

**Autor:** Fernando C.C
**GitHub:** [https://github.com/inventosfer](https://github.com/inventosfer)
