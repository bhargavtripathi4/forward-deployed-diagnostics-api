# Deployment Diagnostics API

A small Python REST API prototype built to demonstrate deployment-readiness basics relevant to Forward Deployed Engineer work: health checks, service status, structured request logs, input validation, and automated endpoint tests.

## Features

- `GET /health` — health check with service name, version, and UTC timestamp.
- `GET /status` — uptime and environment information.
- `POST /diagnostics/echo` — validates a JSON payload and returns a diagnostic response.
- JSON-formatted logs for requests, response status codes, and request duration.
- `X-Request-Duration-Ms` response header.
- Consistent JSON errors for invalid input and unknown routes.
- Automated tests for key success and failure cases.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
python app.py
```

The API starts at `http://127.0.0.1:8000`.

## Try the endpoints

Health check:
```bash
curl http://127.0.0.1:8000/health
```

Service status:
```bash
curl http://127.0.0.1:8000/status
```

Diagnostic request:
```bash
curl -X POST http://127.0.0.1:8000/diagnostics/echo \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: demo-001" \
  -d '{"message":"deployment smoke test"}'
```

On Windows PowerShell, `curl` may be an alias; use `curl.exe` or an API client such as Postman if needed.

## Configuration

Optional environment variables:

- `PORT` — port to listen on (default `8000`)
- `SERVICE_NAME` — service label used in responses and logs
- `APP_VERSION` — version label (default `1.0.0`)
- `APP_ENV` — environment label (default `development`)
- `LOG_LEVEL` — logging level (default `INFO`)

Do not put secrets in source code or commit `.env` files.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Troubleshooting checklist

1. If dependencies fail to install, confirm the intended Python interpreter and virtual environment are active.
2. If the port is busy, set `PORT=8001` and restart the app.
3. If `/health` fails, confirm the process is running and inspect the console logs.
4. If `/diagnostics/echo` returns `400`, verify the request is valid JSON and includes a non-empty string `message`.
5. If a route returns `404`, verify the path and HTTP method.
6. For a real deployment, add platform-specific secret management, HTTPS, authentication, monitoring, and a deployment rollback procedure before exposing it publicly.

## Scope and limitations

This is a learning/demo project, not a production-hardened service. It does not include authentication, persistent storage, or a cloud deployment. Describe it as a local prototype until you have run it, tested it, and optionally deployed it yourself.
