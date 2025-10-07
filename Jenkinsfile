pipeline {
  agent any
  options { timestamps() }

  environment {
    // Cambia esto si tu repo de Docker Hub o tag es otro
    IMAGE = "inventosfer/flask-postgres-compose:latest"
    NAMESPACE = "proyecto-final"
  }

  stages {
    stage('Checkout') {
      steps {
        // Usa la configuración "Pipeline from SCM" del job
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
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker build -t "$IMAGE" .
            docker push "$IMAGE"
          '''
        }
      }
    }

    stage('Kube Deploy') {
      steps {
        // Asegúrate de haber creado la credencial tipo "Secret file" con ID EXACTO 'kubeconfig'
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh '''
            set -eux
            kubectl config use-context minikube

