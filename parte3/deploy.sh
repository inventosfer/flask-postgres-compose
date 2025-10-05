#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="parte2"
DEPLOY="flask-api"
IMAGE="${DOCKERHUB_USER:-inventorfer}/flask-postgres-compose:latest"

echo "[i] Actualizando imagen del deployment ${DEPLOY} a ${IMAGE}"
kubectl -n "${NAMESPACE}" set image deploy/${DEPLOY} ${DEPLOY}="${IMAGE}"

echo "[i] Esperando rollout..."
kubectl -n "${NAMESPACE}" rollout status deploy/${DEPLOY}

echo "[i] Pods actuales:"
kubectl -n "${NAMESPACE}" get pods -l app=${DEPLOY}
