# Task Management API — Project 1

A production-ready **REST API** for task management built with **FastAPI**, **SQLModel**, and **Neon PostgreSQL**. Containerized with a multi-stage Docker build and designed for Kubernetes deployment with full CRUD operations, input validation, filtering, pagination, and a comprehensive test suite.

---

## Features

- **Full CRUD** — Create, List, Get, full Update (PUT), partial Update (PATCH), Delete
- **Priority levels** — 1 (low) to 5 (critical) with server-side validation
- **Filtering** — Filter tasks by completion status (`?completed=true/false`)
- **Pagination** — `offset` and `limit` query parameters on list endpoint
- **Dual database** — Neon PostgreSQL in production, SQLite fallback locally
- **Auto timestamps** — `created_at` and `updated_at` managed by the server
- **Interactive docs** — Swagger UI at `/docs`, ReDoc at `/redoc`
- **Health check** — `GET /health` for liveness probes
- **Docker** — Multi-stage build, non-root user, built-in HEALTHCHECK
- **Tests** — 25+ tests covering happy paths, edge cases, and validation errors

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/tasks` | List all tasks (filter + paginate) |
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks/{id}` | Get a single task |
| `PUT` | `/tasks/{id}` | Full update (all fields required) |
| `PATCH` | `/tasks/{id}` | Partial update (only changed fields) |
| `DELETE` | `/tasks/{id}` | Delete a task |

### Query Parameters — `GET /tasks`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `completed` | `bool` | — | Filter by completion status |
| `offset` | `int` | `0` | Pagination offset |
| `limit` | `int` | `100` | Max results (1–500) |

---

## Task Schema

```json
{
  "id": 1,
  "title": "Write report",
  "description": "Q1 financials",
  "completed": false,
  "priority": 4,
  "created_at": "2026-03-26T10:00:00Z",
  "updated_at": "2026-03-26T10:00:00Z"
}
```

| Field | Type | Constraints |
|---|---|---|
| `title` | string | Required, 1–255 chars |
| `description` | string | Optional, max 2000 chars |
| `completed` | bool | Default: `false` |
| `priority` | int | 1 (low) → 5 (critical), default: `1` |

---

## Project Structure

```
project1/
├── app/
│   ├── main.py          # FastAPI app, route handlers, lifespan
│   ├── models.py        # SQLModel table + request/response schemas
│   ├── crud.py          # Pure database logic (no HTTP concerns)
│   ├── database.py      # DB engine, session factory, table init
│   └── __init__.py
├── tests/
│   ├── conftest.py      # In-memory SQLite fixture + TestClient
│   ├── test_tasks.py    # 25+ CRUD tests (create, read, update, patch, delete)
│   └── test_health.py   # Health endpoint test
├── Dockerfile           # Multi-stage build (builder + runtime)
├── pyproject.toml       # Dependencies, pytest config, build system
└── .env.example         # DATABASE_URL template
```

---

## Local Setup

### 1. Install dependencies

```bash
pip install -e ".[dev]"
```

### 2. Configure database

```bash
cp .env.example .env
# Edit .env and set your DATABASE_URL
# Neon: postgresql+psycopg2://user:pass@ep-xxx.us-east-2.aws.neon.tech/taskdb?sslmode=require
# Local SQLite (no config needed — auto-detected if DATABASE_URL is unset)
```

### 3. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

---

## Running Tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=app --cov-report=term-missing
```

Tests run against an **in-memory SQLite database** — no external dependencies needed.

**Test coverage:**

| Test Class | What it covers |
|---|---|
| `TestCreateTask` | Minimal, full payload, empty title, priority out of range, missing title |
| `TestReadTask` | Empty list, list all, filter completed/pending, pagination, get by ID, 404 |
| `TestUpdateTask` | Full replacement, 404, `updated_at` timestamp advances |
| `TestPatchTask` | Title only, completed toggle, empty body (no-op), 404 |
| `TestDeleteTask` | Delete existing, deleted → 404, delete missing, list shrinks |

---

## Docker

### Build

```bash
docker build -t task-api:1.0.0 .
```

### Run

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg2://user:pass@host/taskdb?sslmode=require" \
  task-api:1.0.0
```

### Docker design

| Feature | Detail |
|---|---|
| Multi-stage build | `builder` installs deps; `runtime` copies only what's needed — minimal image size |
| Non-root user | Runs as `appuser` (UID 1000) — matches `runAsUser: 1000` in Kubernetes |
| HEALTHCHECK | Polls `GET /health` every 30s via stdlib `urllib` (no extra tools) |
| Port | `8000` (uvicorn) |

---

## Example Requests

```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Deploy to production", "priority": 5}'

# List pending tasks
curl "http://localhost:8000/tasks?completed=false"

# Mark a task complete (partial update)
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a task
curl -X DELETE http://localhost:8000/tasks/1
```

---

## Technologies

| Technology | Role |
|---|---|
| **FastAPI** | Web framework — async, auto-validates with Pydantic |
| **SQLModel** | ORM layer — combines SQLAlchemy + Pydantic in one model |
| **Neon PostgreSQL** | Serverless PostgreSQL for production |
| **SQLite** | Zero-config local/test database |
| **uvicorn** | ASGI server |
| **pytest + httpx** | Test framework with FastAPI `TestClient` |
| **Docker** | Multi-stage containerization |
| **Python 3.12** | Runtime |
