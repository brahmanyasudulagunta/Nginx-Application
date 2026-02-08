from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "service": "python-backend",
        "instance": socket.gethostname()
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
