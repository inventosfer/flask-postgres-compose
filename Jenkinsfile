pipeline {
  agent any

  environment {
    // Define en Jenkins → Manage Jenkins → System → Global properties
    // una variable DOCKERHUB_USERNAME con tu usuario de Docker Hub.
    IMAGE_NAME = "${DOCKERHUB_USERNAME ?: ''}/flask-postgres-compose"
    KUBE_NS    = "parte2"
    DEPLOY     = "flask-api"
  }

  options { timestamps() }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Docker Build & Push') {
      environment { DOCKER_CLI_EXPERIMENTAL = "enabled" }
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            if [ -z "$DOCKER_USER" ]; then
              echo "ERROR: define DOCKERHUB_USERNAME como variable global en Jenkins."
              exit 1
            fi
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            cd parte1
            docker build -t "$DOCKER_USER/flask-postgres-compose:latest" .
            docker push "$DOCKER_USER/flask-postgres-compose:latest"
          '''
        }
      }
    }

    stage('Kube Deploy') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh '''
            export KUBECONFIG="$KUBECONFIG"
            kubectl -n "$KUBE_NS" set image deploy/$DEPLOY $DEPLOY="$DOCKER_USER/flask-postgres-compose:latest" || true
            kubectl -n "$KUBE_NS" rollout status deploy/$DEPLOY
            kubectl -n "$KUBE_NS" get pods -l app=$DEPLOY
          '''
        }
      }
    }
  }

  post {
    always { echo "Pipeline finalizado." }
  }
}
