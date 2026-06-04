# Gunicorn Test RPS (Flask)

Simple Flask endpoint to benchmark Gunicorn worker/thread combinations using `wrk`.

## Endpoint

- `GET /?delay_ms=<int>&payload_kb=<int>`
- `delay_ms` (default `0`): sleeps for the given milliseconds before responding.
- `payload_kb` (default `0`): returns an extra payload of `x` bytes to simulate larger responses.
- `GET /healthz`: basic health endpoint.

Example:

```bash
curl "http://127.0.0.1:8000/?delay_ms=250&payload_kb=4"
```

## Run with Docker Compose

```bash
docker compose -f compose.yml up --build
```

Tune Gunicorn with env vars:

```bash
GUNICORN_WORKERS=4 GUNICORN_THREADS=2 docker compose -f compose.yml up --build
```

## Benchmark with wrk

Install `wrk` locally, then run from host:

```bash
wrk -t4 -c64 -d30s "http://127.0.0.1:8000/?delay_ms=0"
wrk -t4 -c64 -d30s "http://127.0.0.1:8000/?delay_ms=50"
wrk -t4 -c64 -d30s "http://127.0.0.1:8000/?delay_ms=200"
```

Try with larger response body:

```bash
wrk -t4 -c64 -d30s "http://127.0.0.1:8000/?delay_ms=50&payload_kb=16"
```

Suggested experiment matrix:

1. Keep `wrk` args fixed (`-t`, `-c`, `-d`).
2. Vary `GUNICORN_WORKERS` and `GUNICORN_THREADS`.
3. For each combination, test `delay_ms=0`, `50`, `200`.
4. Compare `Requests/sec`, latency percentiles, and transfer rate.
