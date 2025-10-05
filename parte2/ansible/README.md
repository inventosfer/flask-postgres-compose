# Parte 2 – Automatización con Ansible

## Objetivo
Automatizar el despliegue de la aplicación Flask + Postgres en un clúster Kubernetes, utilizando Ansible para aplicar todos los manifiestos en orden y asegurar la idempotencia del proceso.

---

## Estructura del directorio
ansible/
├── ansible.cfg          # Configuración básica (usa localhost, sin SSH)
├── inventory.ini        # Inventario con el host local
├── setup-node.yml       # (Opcional) instalación de Docker, kubeadm y kubectl
├── deploy-app.yml       # Playbook principal de despliegue
└── README.md

---

## Descripción de archivos

- ansible.cfg  
  Define la configuración general de Ansible (inventario por defecto, sin comprobación SSH, y salida más legible).

- inventory.ini  
  Lista los hosts donde se ejecutarán las tareas. En este laboratorio, el despliegue se realiza sobre localhost.

- setup-node.yml  
  Playbook opcional para instalar dependencias como Docker, kubectl y kubeadm en un nodo remoto, en caso de necesitar preparar un entorno desde cero.

- deploy-app.yml  
  Playbook principal que aplica todos los manifiestos Kubernetes ubicados en ../k8s, asegurando que se creen en orden lógico (ConfigMap, Secret, PVC, DB, API, Services e Ingress opcional).

---

## Ejecución del playbook

Ejecutar los siguientes comandos desde la carpeta del proyecto:

cd ~/proyectoDevOps/parte2/ansible
ansible-playbook deploy-app.yml

El playbook detecta automáticamente si el namespace parte2 existe, aplica los manifiestos necesarios y espera hasta que los pods estén completamente listos.

---

## Ejemplo de salida

PLAY [Desplegar Flask + Postgres en Kubernetes (namespace parte2)]

TASK [Asegurar namespace]
ok: [localhost]

TASK [ConfigMap]
changed: [localhost]

TASK [Secret]
changed: [localhost]

TASK [PVC DB]
changed: [localhost]

TASK [Deployment DB]
changed: [localhost]

TASK [Service DB]
changed: [localhost]

TASK [Esperar DB lista]
changed: [localhost]

TASK [Deployment API]
changed: [localhost]

TASK [Service API]
changed: [localhost]

TASK [(Opcional) Ingress si existe]
ok: [localhost]

TASK [Esperar API lista]
changed: [localhost]

PLAY RECAP
localhost : ok=11 changed=9 unreachable=0 failed=0 skipped=1 rescued=0 ignored=0

---

## Validación del despliegue

Para comprobar el estado de los recursos creados:

kubectl get pods,svc,pvc -n parte2

Resultado esperado:

NAME                            READY   STATUS    RESTARTS   AGE
pod/flask-api-965df9f97-nj49v   1/1     Running   0          24m
pod/flask-db-57849c8f78-hnmlx   1/1     Running   2          16h

NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/flask-api   ClusterIP   10.101.44.179    <none>        5000/TCP   16h
service/flask-db    ClusterIP   10.101.141.234   <none>        5432/TCP   16h

NAME                                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/postgres-pvc   Bound    pvc-cca959a1-1578-4aed-9a05-3f50b0e50b2f   1Gi        RWO            standard       16h

---

## Conclusión
El despliegue automatizado con Ansible permite aplicar los manifiestos de Kubernetes en el orden correcto, garantizando un entorno reproducible y estable.  
Todos los pods se encuentran en estado Running, y la aplicación responde correctamente a los endpoints /ping, /initdb, /adduser y /users.

