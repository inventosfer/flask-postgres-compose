from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

def get_connection():
    host = os.getenv("DB_HOST", "flask-db")
    port = int(os.getenv("DB_PORT", "5432"))
    db   = os.getenv("DB_NAME", "appdb")
    usr  = os.getenv("DB_USER", "appuser")
    pwd  = os.getenv("DB_PASSWORD", "apppass")
    return psycopg2.connect(host=host, port=port, dbname=db, user=usr, password=pwd)

@app.route("/")
def home():
    return "Flask + Postgres en Kubernetes (Parte 2)\n"

@app.route("/ping")
def ping():
    return jsonify(status="ok")

@app.route("/initdb")
def initdb():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return "Tabla 'users' creada (si no existía)."
    except Exception as e:
        return f"Error initdb: {e}", 500

@app.route("/adduser/<name>")
def adduser(name):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()
        cur.close()
        conn.close()
        return f"Usuario '{name}' insertado."
    except Exception as e:
        return f"Error adduser: {e}", 500

@app.route("/users")
def list_users():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        data = [{"id": r[0], "name": r[1]} for r in rows]
        return jsonify(data)
    except Exception as e:
        return f"Error users: {e}", 500

if __name__ == "__main__":
    # Local/dev: no se usa en K8s (allí ejecuta gunicorn), pero dejamos por si acaso
    app.run(host="0.0.0.0", port=5000)

