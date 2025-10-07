#!/bin/bash
# Script de validación de Pods y Services (check.sh)
# Autor: Fer

NAMESPACE="parte2"

echo "======================================="
echo "     Validando estado de los Pods"
echo "======================================="
kubectl -n $NAMESPACE get pods

if kubectl -n $NAMESPACE get pods | grep -v NAME | grep -qv Running; then
  echo "ERROR: Algún Pod no está en estado Running"
  exit 1
else
  echo "OK: Todos los Pods están en estado Running"
fi

echo ""
echo "======================================="
echo "    Validando estado de los Services"
echo "======================================="
kubectl -n $NAMESPACE get svc

if kubectl -n $NAMESPACE get svc | grep -v NAME | grep -qv ClusterIP; then
  echo "  ERROR: Algún Service no se ha creado correctamente"
  exit 1
else
  echo "  OK: Los Services están activos"
fi

echo ""
echo " Validación completada correctamente"
