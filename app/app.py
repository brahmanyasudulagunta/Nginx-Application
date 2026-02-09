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
    user="kishna",
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

    cached = redis_client.get("visits")
    if cached:
        visits = int(cached)
    else:
        cursor = pg_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INT)")
        cursor.execute("INSERT INTO visits (count) VALUES (1) ON CONFLICT DO NOTHING")
        cursor.execute("UPDATE visits SET count = count + 1")
        pg_conn.commit()
        cursor.execute("SELECT count FROM visits LIMIT 1")
        visits = cursor.fetchone()[0]
        redis_client.setex("visits", 10, visits)

    return jsonify({
        "instance": hostname,
        "visits": visits
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
