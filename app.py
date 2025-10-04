from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Datos de conexión (los mismos que definiste en docker-compose.yml)
DB_HOST = "db"
DB_PORT = "5432"
DB_NAME = "appdb"
DB_USER = "appuser"
DB_PASSWORD = "apppass"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def home():
    return "Flask + Gunicorn + Nginx + Postgres funcionando!"

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})

@app.route("/initdb")
def initdb():
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
    return "Tabla 'users' creada en Postgres (si no existía)."

@app.route("/adduser/<name>")
def adduser(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Usuario '{name}' insertado."

@app.route("/users")
def list_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

