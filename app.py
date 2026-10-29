import json
import logging
import os
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(message)s")
logger = logging.getLogger("deployment_diagnostics")
START_TIME = time.time()
SERVICE_NAME = os.getenv("SERVICE_NAME", "deployment-diagnostics-api")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

def log_event(event, **fields):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": SERVICE_NAME,
        "event": event,
        **fields,
    }
    logger.info(json.dumps(record, default=str))

@app.before_request
def log_request_start():
    request._started_at = time.time()

@app.after_request
def log_request_end(response):
    elapsed_ms = round((time.time() - getattr(request, "_started_at", time.time())) * 1000, 2)
    log_event(
        "http_request",
        method=request.method,
        path=request.path,
        status_code=response.status_code,
        duration_ms=elapsed_ms,
    )
    response.headers["X-Request-Duration-Ms"] = str(elapsed_ms)
    return response

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": SERVICE_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }), 200

@app.get("/status")
def status():
    return jsonify({
        "service": SERVICE_NAME,
        "version": APP_VERSION,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "environment": os.getenv("APP_ENV", "development"),
    }), 200

@app.post("/diagnostics/echo")
def diagnostics_echo():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400
    if "message" not in payload:
        return jsonify({"error": "Missing required field: message"}), 400
    message = payload["message"]
    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Field 'message' must be a non-empty string"}), 400
    log_event("diagnostics_echo", message_length=len(message))
    return jsonify({"ok": True, "message": message, "request_id": request.headers.get("X-Request-ID")}), 200

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Route not found", "path": request.path}), 404

@app.errorhandler(500)
def internal_error(_error):
    log_event("internal_error", path=request.path)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
