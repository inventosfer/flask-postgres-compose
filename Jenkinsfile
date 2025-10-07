pipeline {
  agent any
  options { timestamps() }

  environment {
    IMAGE       = "inventosfer/flask-postgres-compose:latest"
    NAMESPACE   = "parte2"
    DOCKERFILE  = "parte1/Dockerfile"
    CONTEXT     = "parte1"
    MANIFESTS   = "parte2/k8s"
    KUBECONFIG  = "/var/jenkins_home/.kube/config"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Sanity') {
      steps {
        sh '''
bash -lc '
  set -euo pipefail
  echo "--- Raíz del repo ---"; pwd
  echo "--- Dockerfile(s) ---"; find . -maxdepth 3 -iname Dockerfile -print || true
  echo "--- YAMLs ---"; find . -maxdepth 3 -name "*.yaml" -print | head -n 100 || true
'
        '''
      }
    }

    stage('Docker Build & Push') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'dockerhub',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh '''
bash -lc '
  set -euo pipefail
  echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
  docker build -t ${IMAGE} -f ${DOCKERFILE} ${CONTEXT}
  docker push ${IMAGE}
'
          '''
        }
      }
    }

    stage('Kube Deploy') {
      when { expression { return fileExists(env.MANIFESTS) } }
      steps {
        sh '''
bash -lc '
  set -euo pipefail
  echo ">>> kubeconfig: $KUBECONFIG | context: $(kubectl config current-context) <<<"
  kubectl get ns || true

  # Asegura el namespace
  kubectl get ns ${NAMESPACE} || kubectl create ns ${NAMESPACE}

  # Quita metadata.namespace de los YAML por seguridad
  find ${MANIFESTS} -name "*.yaml" -exec sed -i "/^[[:space:]]*namespace:/d" {} \\;

  # Aplica manifests directamente en el namespace
  kubectl -n ${NAMESPACE} apply -f ${MANIFESTS}

  # Fuerza imagen conocida y espera rollout de la API
  kubectl -n ${NAMESPACE} set image deploy/flask-api flask-api=${IMAGE} || true
  kubectl -n ${NAMESPACE} rollout status deploy/flask-api --timeout=180s

  # Estado inmediato
  kubectl -n ${NAMESPACE} get all
'
        '''
      }
    }

    stage('Stabilize Pods') {
      steps {
        sh '''
bash -lc '
  set -euo pipefail

  # Espera hasta que TODOS los pods estén en STATUS Running
  for i in {1..24}; do
    not_running=$(kubectl -n ${NAMESPACE} get pods --no-headers | awk '"'"'$3!="Running"{c++} END{print c+0}'"'"')
    [ "${not_running}" -eq 0 ] && break
    echo "Esperando estabilización... pods no Running=${not_running}"
    sleep 5
  done

  echo "--- Estado final de pods ---"
  kubectl -n ${NAMESPACE} get pods
'
        '''
      }
    }

    stage('Check Pods & Services') {
      steps {
        sh '''
bash -lc '
  set -euo pipefail
  chmod +x ./check.sh || true
  ./check.sh
'
        '''
      }
    }
  }

  post {
    success { echo ' Pipeline OK — listo para el pantallazo' }
    failure { echo ' Falló — revisa el final del log' }
  }
}

