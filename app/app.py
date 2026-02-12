from flask import Flask, jsonify
import socket
import psycopg2
import mysql.connector
import redis
import os
import time

app = Flask(__name__)

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

pg_conn = None
mysql_conn = None

def get_pg_conn():
    global pg_conn
    if pg_conn is None or pg_conn.closed:
        for i in range(10):
            try:
                pg_conn = psycopg2.connect(
                    host="postgres",
                    database="postgresdb",
                    user="krishna",
                    password="1729"
                )
                print("Connected to PostgreSQL")
                break
            except Exception as e:
                print(f"Waiting for PostgreSQL... ({e})")
                time.sleep(2)
    return pg_conn

def get_mysql_conn():
    global mysql_conn
    if mysql_conn is None or not mysql_conn.is_connected():
        for i in range(10):
            try:
                mysql_conn = mysql.connector.connect(
                    host="mysql",
                    user="rama",
                    password="1729",
                    database="mysqldb"
                )
                print("Connected to MySQL")
                break
            except Exception as e:
                print(f"Waiting for MySQL... ({e})")
                time.sleep(2)
    return mysql_conn

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
    conn = get_pg_conn()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INT)")
    cursor.execute("SELECT count FROM visits")

    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO visits (count) VALUES (1)")
        visits = 1
    else:
        cursor.execute("UPDATE visits SET count = count + 1")
        visits = row[0] + 1

    conn.commit()

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
