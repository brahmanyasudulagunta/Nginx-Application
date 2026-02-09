from flask import Flask, jsonify
import socket
import psycopg2
import mysql.connector
import redis
import os

app = Flask(__name__)

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

pg_conn = psycopg2.connect(
    host="postgres",
    database="postgresdb",
    user="krishna",
    password="1729"
)

mysql_conn = mysql.connector.connect(
    host="mysql",
    user="rama",
    password="1729",
    database="mysqldb"
)

@app.route("/")
def home():
    hostname = socket.gethostname()
    visits = None

    # 1. Try Redis (optional dependency)
    try:
        cached = redis_client.get("visits")
        if cached:
            return jsonify({
                "instance": hostname,
                "visits": int(cached),
                "source": "redis-cache"
            })
    except Exception as e:
        print(f"Redis unavailable: {e}")

    # 2. Fallback to PostgreSQL (critical dependency)
    cursor = pg_conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INT)")
    cursor.execute("SELECT count FROM visits")

    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO visits (count) VALUES (1)")
        visits = 1
    else:
        cursor.execute("UPDATE visits SET count = count + 1")
        visits = row[0] + 1

    pg_conn.commit()

    # 3. Try to refresh Redis (best-effort)
    try:
        redis_client.setex("visits", 10, visits)
    except Exception as e:
        print(f"Redis set failed: {e}")

    return jsonify({
        "instance": hostname,
        "visits": visits,
        "source": "postgres"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
