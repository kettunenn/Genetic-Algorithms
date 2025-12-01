from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_DIR = os.path.abspath("./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/ping")
def ping():
    return jsonify({"status": "ok"})

@app.post("/upload")
def upload():
    if "file" not in request.files:
        return jsonify({"error": "missing 'file' field"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "empty filename"}), 400
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    safe_name = f.filename.replace("/", "_")
    out_path = os.path.join(UPLOAD_DIR, f"{ts}-{safe_name}")
    f.save(out_path)
    return jsonify({"saved": out_path})

if __name__ == "__main__":
    # Listen on all interfaces so your device can reach it
    app.run(host="0.0.0.0", port=5000)