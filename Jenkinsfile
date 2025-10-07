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
          set -eux
          echo "--- Raíz del repo ---"; pwd
          echo "--- Dockerfile(s) ---"; find . -maxdepth 3 -iname Dockerfile -print || true
          echo "--- YAMLs ---"; find . -maxdepth 3 -name "*.yaml" -print | head -n 100 || true
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
            set -eux
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker build -t ${IMAGE} -f ${DOCKERFILE} ${CONTEXT}
            docker push ${IMAGE}
          '''
        }
      }
    }

    stage('Kube Deploy') {
      when { expression { return fileExists(env.MANIFESTS) } }
      steps {
        sh '''
          set -eux
          echo ">>> kubeconfig: $KUBECONFIG | context: $(kubectl config current-context) <<<"
          kubectl get ns || true

          # Asegura el namespace
          kubectl get ns ${NAMESPACE} || kubectl create ns ${NAMESPACE}

          # Quita metadata.namespace de todos los YAML (por si acaso)
          find ${MANIFESTS} -name "*.yaml" -exec sed -i '/^[[:space:]]*namespace:/d' {} \\;

          # Aplica directamente en el namespace (sin kustomize)
          kubectl -n ${NAMESPACE} apply -f ${MANIFESTS}

          # Fuerza imagen conocida y espera rollout
          kubectl -n ${NAMESPACE} set image deploy/flask-api flask-api=${IMAGE} || true
          kubectl -n ${NAMESPACE} rollout status deploy/flask-api --timeout=180s

          # Estado final
          kubectl -n ${NAMESPACE} get all
        '''
      }
    }

    stage('Check Pods & Services') {
      steps {
        sh '''
          chmod +x ./check.sh || true
          ./check.sh
        '''
      }
    }
  }

  post {
    success { echo ' Pipeline OK — listo para el pantallazo' }
    failure { echo ' Falló — revisa el final del log' }
  }
}

