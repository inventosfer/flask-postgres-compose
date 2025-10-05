# Parte 2 – Despliegue en Kubernetes

## Objetivo
Desplegar la aplicación Flask + Postgres en un clúster Kubernetes con persistencia y servicios internos.


---

## Arquitectura del despliegue

```text
Cliente (curl / navegador)
        │
        ▼
Service (ClusterIP :8080)
        │
        ▼
Gunicorn (5000) → Flask (Python API)
        │
        ▼
PostgreSQL (5432)
        │
        ▼
PersistentVolumeClaim (1Gi)

```


## Archivos principales
- `deploy-api.yaml`
- `deploy-db.yaml`
- `svc-api.yaml`
- `svc-db.yaml`
- `pvc-db.yaml`
- `configmap.yaml`
- `secret.yaml`

> Nota: `configmap.yaml` proporciona la configuración de la aplicación (por ejemplo, variables no sensibles).  
> `secret.yaml` gestiona credenciales o valores sensibles (por ejemplo, usuario y contraseña de la base de datos).  
> Ambos son referenciados desde los deployments correspondientes.


## Despliegue (orden recomendado)

```bash
# Namespace (si no existe)
kubectl create namespace parte2 2>/dev/null || true

# Recursos base
kubectl apply -n parte2 -f configmap.yaml
kubectl apply -n parte2 -f secret.yaml
kubectl apply -n parte2 -f pvc-db.yaml

# Base de datos y servicio
kubectl apply -n parte2 -f deploy-db.yaml
kubectl apply -n parte2 -f svc-db.yaml

# API y servicio
kubectl apply -n parte2 -f deploy-api.yaml
kubectl apply -n parte2 -f svc-api.yaml

```


## Comandos ejecutados y resultados

A continuación se muestran los comandos utilizados para verificar el despliegue y su salida real:

```bash
# Verificación de pods, servicios y volúmenes
fer@ubuntu24:~/parte2/k8s$ kubectl get pods,svc,pvc -n parte2
NAME                            READY   STATUS    RESTARTS      AGE
pod/flask-api-b4d97c48d-sz5l6   1/1     Running   0             5m15s
pod/flask-db-57849c8f78-hnmlx   1/1     Running   1 (10h ago)   11h

NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/flask-api   ClusterIP   10.101.44.179    <none>        5000/TCP   11h
service/flask-db    ClusterIP   10.101.141.234   <none>        5432/TCP   11h

NAME                                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/postgres-pvc   Bound    pvc-cca959a1-1578-4aed-9a05-3f50b0e50b2f   1Gi        RWO            standard       <unset>                 11h

# Logs del API Flask
fer@ubuntu24:~/parte2/k8s$ kubectl logs deploy/flask-api -n parte2 | tail -n 30
[2025-10-05 11:19:04 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-10-05 11:19:04 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2025-10-05 11:19:04 +0000] [1] [INFO] Using worker: sync
[2025-10-05 11:19:04 +0000] [6] [INFO] Booting worker with pid: 6

# Logs de la base de datos PostgreSQL
fer@ubuntu24:~/parte2/k8s$ kubectl logs deploy/flask-db -n parte2 | tail -n 30
PostgreSQL Database directory appears to contain a database; Skipping initialization
...
2025-10-05 11:21:11.735 UTC [28] LOG:  checkpoint complete: wrote 49 buffers ...

# Test de los endpoints
fer@ubuntu24:~/parte2/k8s$ curl http://localhost:8080/ping
{"status":"ok"}

fer@ubuntu24:~/parte2/k8s$ curl http://localhost:8080/users
[{"id":1,"name":"Fer"},{"id":2,"name":"Fer"}]
