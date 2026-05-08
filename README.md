# AI-Native Task Manager

An AI-native task management ecosystem where autonomous agents collaborate to handle reminders, appointments, notifications, and productivity workflows — naturally and reliably.

> **New here?** Read [`AGENTS.md`](./AGENTS.md) — our project constitution. It explains *how* we work (ethos, principles, workflow) before *what* we build.

---

## Why This Project

Most task managers make you do the work of being organized — typing forms, setting reminders, juggling calendars. We think a task manager should *understand* you instead. You say _"remind me to call Sara at 8 PM tomorrow"_ and the system handles the rest: parses intent, schedules, notifies, follows up, learns.

Under the hood, that means a small team of focused AI agents — each with a clear job — coordinating through well-defined tools.

---

## What's in This Repo

This repository is a **monorepo** that grows project-by-project toward the full vision. Each project is a self-contained, production-quality slice that ships to a Kubernetes cluster.

| Project | Status | Description |
|---|---|---|
| [Project 1 — Task API](./docs/project-1.md) | ✅ Shipped | FastAPI + SQLModel + Postgres CRUD service. The system of record for tasks. |
| Project 2 — Tasks Manager Agent | 🛠️ Next | OpenAI Agents SDK orchestrator that turns natural language into task operations. |
| Project 3 — Notifications API | 📋 Planned | Multi-channel reminder delivery (email / SMS / push). |
| Project 4 — Appointment Booking Agent | 📋 Planned | Specialized agent for booking workflows. |

The roadmap will expand as projects land.

---

## Quick Start (Project 1 — Task API)

```bash
# Install dependencies
pip install -e ".[dev]"

# Run the API
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000/docs** for interactive API docs.

Full setup, schema, Docker, and test details: [`docs/project-1.md`](./docs/project-1.md).

---

## How We Work

A few highlights from [`AGENTS.md`](./AGENTS.md) — read it in full before contributing:

- **Test-Driven Development.** Failing test first, then code, then refactor.
- **Cloud-native from day one.** Every service ships as a container, runs on Kubernetes, mirrored locally with kind/k3d.
- **Official docs are the source of truth.** Read the current SDK/framework docs before writing code against them — never rely on memory.
- **Prefer agent skills and MCP** over hand-rolled integrations.
- **Production-first mindset.** No "we'll harden it later." Logs, metrics, traces, and probes are part of the feature, not an afterthought.

---

## Tech Stack (Target)

| Layer | Technology |
|---|---|
| Frontend | Next.js |
| AI Agent Framework | OpenAI Agents SDK |
| Tool Protocol | Model Context Protocol (MCP) |
| Backend APIs | FastAPI |
| Auth | Better Auth |
| Database | PostgreSQL (Neon) / SQLite locally |
| Scheduling | APScheduler / Celery |
| Containerization | Docker (multi-stage) |
| Orchestration | Kubernetes (Helm) |

---

## Contributing

1. Read [`AGENTS.md`](./AGENTS.md) — the constitution. Non-negotiable starting point.
2. Pick (or open) an issue scoped to a single vertical slice.
3. Branch off `main`, write the failing test, then the code.
4. Open a pull request. CI must be green; a reviewer signs off.

Disagreements about the constitution are welcome — amend it through a PR that explains what's changing and why.

---

## License

TBD.

---

## Maintainer

[@rashid200gb](https://github.com/rashid200gb)
