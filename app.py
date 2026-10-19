import os
import time
import mysql.connector
from flask import Flask

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
                "CREATE TABLE IF NOT EXISTS kunjungan ("
                "id INT AUTO_INCREMENT PRIMARY KEY, "
                "waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
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
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO kunjungan () VALUES ()")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM kunjungan")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f"Halo dari Flask + Docker + Jenkins! Terhubung ke MySQL. Total kunjungan tersimpan di database: {total}"


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)