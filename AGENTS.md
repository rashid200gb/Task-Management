# AGENTS.md — Project Constitution

> This document is the **constitution** of the AI-Native Task Manager.
> It describes **how we work**, not what we build.
> It is intentionally free of JSON schemas, API contracts, and implementation details — those live in code and in the official docs of the libraries we use.

---

## 1. Mission

Build an AI-native task management ecosystem where autonomous agents collaborate to manage reminders, appointments, notifications, and productivity workflows — naturally, reliably, and at production quality from day one.

---

## 2. Ethos — How We Work

These are the values every contributor (human or agent) is expected to uphold.

1. **Production-first mindset.** Every feature is written as if it ships to a real user tomorrow. No "we'll harden it later."
2. **Cloud-native by default.** The system is designed from the very first commit to run on a Kubernetes cluster. Local development must mirror that target.
3. **Source of truth is the official docs.** Before writing code against any SDK, framework, or protocol, read its current official documentation. Do not rely on training data, blog posts, or stale memory.
4. **Lean on the platform, don't reimplement it.** Prefer using a capability through an existing **agent skill** or an **MCP server** over hand-rolling integrations.
5. **Small, reversible steps.** Ship narrow vertical slices end-to-end. Avoid big-bang refactors and speculative abstractions.
6. **Honesty over optimism.** Surface unknowns, risks, and failures early. A working "I don't know yet" beats a confident guess.
7. **Readable beats clever.** Code is read far more than it is written. Choose clarity.
8. **Security and privacy are non-negotiable.** Treat every input as untrusted and every secret as production-sensitive, even in dev.

---

## 3. Programming Principles

### 3.1 Test-Driven Development (TDD)
- Write the failing test first. Then write the smallest code that makes it pass. Then refactor.
- Every behavior an agent or API exposes must be covered by an automated test before it is considered "done."
- Tests describe intent — they are the executable specification of the system.

### 3.2 Design Principles
- **SOLID** for object/module boundaries.
- **YAGNI** — don't build what isn't required by a current test or user story.
- **DRY**, but only after the third repetition. Premature abstraction is worse than duplication.
- **Twelve-Factor App** discipline — config in env, stateless processes, explicit dependencies, logs as event streams.

### 3.3 Code Quality Bar
- Type hints everywhere in Python; strict TypeScript on the frontend.
- All I/O is async unless there is a documented reason not to.
- Errors are values to be handled, not exceptions to be ignored.
- Structured logging only — every log line is machine-parsable.
- No dead code, no commented-out code, no TODOs without an owner and a date.

### 3.4 Definition of Done
A change is done when **all** of these are true:
- Tests written first, and now passing.
- Linter and type checker are clean.
- Runs locally against the same container image that will run in the cluster.
- Observability hooks (logs, metrics, traces) are in place.
- Documentation in the relevant module is updated.
- A reviewer (human or agent) has signed off.

---

## 4. Development Workflow

### 4.1 Always Consult Official Documentation
Before introducing or upgrading any dependency — OpenAI Agents SDK, MCP SDK, FastAPI, Next.js, Better Auth, APScheduler, Kubernetes APIs, etc. — read its **current official documentation**. Pin the version you read against. If behavior contradicts what you remember, the docs win.

### 4.2 Prefer Agent Skills and MCP
When building a new capability:
1. Check whether an existing **agent skill** already does the job.
2. Check whether an **MCP server** exposes the capability.
3. Only if neither exists, write a new tool — and expose it through MCP so the rest of the system can reuse it.

This keeps the agent surface composable and avoids one-off integrations.

### 4.3 Branching and Review
- Trunk-based development with short-lived feature branches.
- Every change goes through pull request review, even for solo work — the review forces a second pass.
- CI must be green before merge. Red CI blocks the queue.

### 4.4 Observability is Part of the Feature
A feature without logs, metrics, and traces is not finished. We debug production from telemetry, not from guesses.

---

## 5. Deployment — Kubernetes from Day One

The final target is a **Kubernetes cluster**, and the project is structured around that fact from the very first commit.

### 5.1 Cluster-Ready Principles
- Every service ships as a container image built from a reproducible Dockerfile.
- Every service has a liveness probe, a readiness probe, and a graceful shutdown path.
- All configuration is supplied via environment variables and Kubernetes `ConfigMap` / `Secret` objects — never baked into images.
- Services are stateless; persistence lives in managed databases or `PersistentVolumeClaim`s, never on the pod filesystem.
- Resource requests and limits are declared for every workload.
- Horizontal scaling is the default scaling strategy.

### 5.2 Local Development Mirrors Production
- Local dev runs against the same container images using a local cluster (kind, k3d, or minikube).
- Helm charts (or equivalent manifests) are the single source of truth for how a service is deployed — locally and in production.
- "Works on my machine" is not an acceptable status; "works on the cluster" is.

### 5.3 Operability
- Centralized logging, metrics, and tracing are wired up before a service is considered launched.
- Rollouts are progressive (rolling updates, with the ability to roll back).
- Secrets are managed through a proper secret store, never committed.

---

## 6. Security and Privacy

- Validate every input crossing a trust boundary — user, network, agent tool call.
- Least privilege for every credential, service account, and RBAC binding.
- Encrypt data in transit and at rest.
- Audit agent actions: every tool invocation is logged with enough context to reconstruct what the agent did and why.
- Treat AI prompts and tool outputs as untrusted content — defend against prompt injection at every boundary.

---

## 7. Collaboration Norms

- Default to writing things down. If a decision matters, it lives in the repo, not in chat.
- Disagree, then commit. Argue the idea, support the decision.
- Optimize for the next person reading the code — that person is often you, six months later.
- Ask for help early. A 15-minute question beats a two-day detour.

---

## 8. Amending This Constitution

This document is living. Amend it through a pull request that explains:
- What is changing.
- Why the current rule no longer serves us.
- What the new rule is.

Once merged, the new rule applies to all subsequent work.
