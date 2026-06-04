import os
import threading
import time

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def benchmark_endpoint():
    """
    Example:
      /?delay_ms=100&payload_kb=4
    """
    delay_ms = request.args.get("delay_ms", default=0, type=int)
    payload_kb = request.args.get("payload_kb", default=0, type=int)

    if delay_ms > 0:
        time.sleep(delay_ms / 1000)

    payload = "x" * (payload_kb * 1024)
    now = time.time()

    return jsonify({
        "ok": True,
        "delay_ms": delay_ms,
        "payload_kb": payload_kb,
        "server_pid": os.getpid(),
        "thread": threading.current_thread().name,
        "ts": now,
        "payload": payload,
    })


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
