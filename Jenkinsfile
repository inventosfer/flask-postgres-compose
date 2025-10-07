pipeline {
  agent any
  options { timestamps() }

  environment {
    IMAGE     = "inventosfer/flask-postgres-compose:latest"   // ajusta si usas otro repo/tag
    NAMESPACE = "proyecto-final"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
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
            echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
            docker build -t ${env.IMAGE} .
            docker push ${env.IMAGE}
          """
        }
      }
    }

    stage('Kube Deploy') {
      steps {
        // Credencial tipo Secret file con ID EXACTO 'kubeconfig'
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh """
            set -eux
            kubectl config use-context minikube
            kubectl create ns ${env.NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
            kubectl -n ${env.NAMESPACE} apply -f parte2/k8s/
            kubectl -n ${env.NAMESPACE} get all
          """
        }
      }
    }
  }

  post {
    always { echo 'Pipeline finalizado.' }
  }
}

