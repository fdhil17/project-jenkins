import os
import time
import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_conn():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "appuser"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "appdb"),
    )


def init_db():
    for _ in range(30):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS notes ("
                "id INT AUTO_INCREMENT PRIMARY KEY, "
                "content VARCHAR(255) NOT NULL, "
                "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except mysql.connector.Error:
            time.sleep(2)
    raise RuntimeError("Database tidak dapat dihubungi")


@app.route("/")
def index():
    return "Halo dari Flask + MySQL + Docker + Jenkins!"


@app.route("/notes", methods=["GET"])
def list_notes():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json(silent=True) or {}
    content = str(data.get("content", "")).strip()
    if not content:
        return jsonify(error="content wajib diisi"), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(message="tersimpan"), 201


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)