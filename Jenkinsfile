pipeline {
  agent any
  options { timestamps() }

  environment {
    IMAGE       = "inventosfer/flask-postgres-compose:latest"
    NAMESPACE   = "proyecto-final"

    DOCKERFILE  = "parte1/Dockerfile"   // <- tu Dockerfile
    CONTEXT     = "parte1"              // <- carpeta del build context
    MANIFESTS   = "parte2/k8s"          // <- manifiestos K8s
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Sanity') {
      steps {
        sh '''
          set -eux
          pwd; echo "--- raíz del repo ---"; ls -la
          echo "--- Dockerfile(s) ---"; find . -maxdepth 3 -iname Dockerfile -print || true
          echo "--- YAMLs ---"; find . -maxdepth 3 -name "*.yaml" -print | head -n 50 || true
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
          sh """
            set -eux
            echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
            docker build -t \${IMAGE} -f \${DOCKERFILE} \${CONTEXT}
            docker push \${IMAGE}
          """
        }
      }
    }

    stage('Kube Deploy') {
      when { expression { return fileExists(env.MANIFESTS) } }
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh """
            set -eux
            kubectl config use-context minikube
            kubectl create ns \${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
            kubectl -n \${NAMESPACE} apply -f \${MANIFESTS}
            kubectl -n \${NAMESPACE} get all
          """
        }
      }
    }
  }

  post { always { echo 'Pipeline finalizado.' } }
}
