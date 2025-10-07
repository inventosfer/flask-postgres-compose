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
      steps {
        checkout scm
      }
    }

    stage('Sanity') {
      steps {
        sh '''
          set -eux
          echo "--- Raíz del repo ---"
          pwd
          echo "--- Dockerfile(s) ---"
          find . -maxdepth 3 -iname Dockerfile -print || true
          echo "--- YAMLs ---"
          find . -maxdepth 3 -name "*.yaml" -print | head -n 100 || true
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
          echo ">>> Usando kubeconfig en: $KUBECONFIG <<<"

          kubectl config current-context
          kubectl get ns || true

          # Crea namespace si no existe
          kubectl get ns ${NAMESPACE} || kubectl create ns ${NAMESPACE}

          # Elimina líneas namespace: de los YAML
          find ${MANIFESTS} -name "*.yaml" -exec sed -i '/^[[:space:]]*namespace:/d' {} \\;

          # Directorio temporal para Kustomize
          tmpdir=$(mktemp -d)
          manifest_abs=$(realpath ${MANIFESTS})

          cat > "$tmpdir/kustomization.yaml" <<EOF
namespace: ${NAMESPACE}
resources:
- ${manifest_abs}
EOF

          echo "--- kustomization.yaml ---"
          cat "$tmpdir/kustomization.yaml"

          kubectl apply --validate=false -k "$tmpdir"

          # Forzar imagen conocida y esperar rollout
          kubectl -n ${NAMESPACE} set image deploy/flask-api flask-api=${IMAGE}
          kubectl -n ${NAMESPACE} rollout status deploy/flask-api --timeout=180s

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
    always {
      echo '✅ Pipeline finalizado correctamente.'
    }
  }
}

