from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "service": "python-backend",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
