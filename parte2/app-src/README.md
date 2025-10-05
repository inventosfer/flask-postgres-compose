# Entrega 1 – Parte 1: Preparación y Docker/Compose

##  Objetivo
- Crear aplicación base con Flask.
- Gestionar versiones con Git.
- Construir imágenes Docker y usar Docker Compose.
- Incluir servicio web (Flask con Gunicorn) y base de datos (Postgres).
- Añadir persistencia de datos.
- Probar acceso en navegador `http://localhost:8080`.

---

##  Estructura del proyecto


```

.
├── app.py
├── docker-compose.yml
├── Dockerfile
├── nginx
│   └── nginx.conf
├── README.md
└── requirements.txt

```


---

##  Configuración de servicios

###  Web
- Framework: Flask
- Servidor WSGI: Gunicorn
- Rutas disponibles:
  - `/` → mensaje de bienvenida
  - `/ping` → respuesta JSON con `{"status":"ok"}`
  - `/initdb` → crea tabla `users`
  - `/adduser/<nombre>` → inserta usuario en la tabla
  - `/users` → lista usuarios en formato JSON

### 🔹 Base de datos
- Imagen: `postgres:16`
- Variables:
  - `POSTGRES_DB=appdb`
  - `POSTGRES_USER=appuser`
  - `POSTGRES_PASSWORD=apppass`
- Persistencia: volumen `pgdata:/var/lib/postgresql/data`

### 🔹 Nginx
- Imagen: `nginx:alpine`
- Función: proxy inverso hacia el servicio Flask
- Escucha en puerto **8080**

---

##  Pasos de uso

### 1. Construcción y despliegue
```bash
# Inicializar repo Git (se puede hacer al final)
git init
git add .
git commit -m "Entrega 1: Flask + Postgres con Docker Compose"

# Levantar servicios
docker compose up -d --build

# Ver estado
docker compose ps


curl http://localhost:8080/
curl http://localhost:8080/ping
curl http://localhost:8080/initdb
curl http://localhost:8080/adduser/Fer
curl http://localhost:8080/users
```  

## Evidencia
Se incluyen las siguientes capturas en la entrega:
1. Salida de `docker compose ps`.

NAME             IMAGE          COMMAND                  SERVICE   CREATED          STATUS          PORTS
flask-nginx      nginx:alpine   "/docker-entrypoint.…"   nginx     20 minutes ago   Up 20 minutes   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
flask-postgres   postgres:16    "docker-entrypoint.s…"   db        20 minutes ago   Up 20 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
flask-web        test-web       "gunicorn -b 0.0.0.0…"   web       20 minutes ago   Up 20 minutes   5000/tcp

2. Acceso en navegador a `http://localhost:8080/`.

Flask + Gunicorn + Nginx + Postgres funcionando!


3. Respuesta de `/ping`.

{"status":"ok"}

4. Respuesta de `/users` después de añadir un usuario.

[{"id":1,"name":"Fernando"},{"id":2,"name":"Pepe"},{"id":3,"name":"Luis"},{"id":4,"name":"Jaime"},{"id":5,"name":"Anna"},{"id":6,"name":"users"}]


---

## Gestión con Git

Se inicializó el repositorio en la carpeta del proyecto y se realizó el primer commit:

```bash
git init
git add .
git commit -m "Entrega 1: Flask + Postgres con Docker Compose"

git log --oneline
94d1c54 (HEAD -> main) Parte 1: Flask + Postgres con Docker Compose



---

## Repositorio en GitHub
El código de este proyecto está disponible en:  
  [https://github.com/inventorfer/flask-postgres-compose](https://github.com/inventorfer/flask-postgres-compose)
