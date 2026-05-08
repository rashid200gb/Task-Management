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

1. **Always verify what you are doing.** Every claim, every change, every "done" must be checked against reality — run the test, read the file, hit the endpoint, query the cluster. Plausible is not the same as correct. If you cannot verify it, say so.
2. **Production-first mindset.** Every feature is written as if it ships to a real user tomorrow. No "we'll harden it later."
3. **Cloud-native by default.** The system is designed from the very first commit to run on a Kubernetes cluster. Local development must mirror that target.
4. **Source of truth is the official docs.** Before writing code against any SDK, framework, or protocol, read its current official documentation. Do not rely on training data, blog posts, or stale memory.
5. **Lean on the platform, don't reimplement it.** Prefer using a capability through an existing **agent skill** or an **MCP server** over hand-rolling integrations.
6. **Small, reversible steps.** Ship narrow vertical slices end-to-end. Avoid big-bang refactors and speculative abstractions.
7. **Honesty over optimism.** Surface unknowns, risks, and failures early. A working "I don't know yet" beats a confident guess.
8. **Readable beats clever.** Code is read far more than it is written. Choose clarity.
9. **Security and privacy are non-negotiable.** Treat every input as untrusted and every secret as production-sensitive, even in dev.

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

## 8. Agent-Building Discipline

These practices apply when a contributor (human or AI agent) is *building, prompting, or operating* an agent inside this system. Adapted from the Panaversity Agent Factory _Creator Workflow_ guidance.

### 8.1 Plan Before You Execute
- For any non-trivial change, write the plan first — what you intend to do, why, what could break.
- Iterate on the plan until it is solid. Do not skip planning to "save time"; rework caused by skipping it costs more.
- Re-plan immediately when execution goes sideways. Do not push through a flawed plan because you've already started.

### 8.2 Two-Pass Verification
- For critical work, separate the author and the reviewer. The reviewer reads with fresh eyes — no sunk-cost bias.
- Reviewer asks: "What would make this fail? What is the author *not* showing me?"
- Address review feedback before merging.

### 8.3 Build Verification Into the Loop
- Every agent and every service must have a way to verify its own output: a test command, a smoke endpoint, a metric query, a sample run.
- "Plausible output" is not "correct output." If there is no way to verify, build one before shipping.
- Wire verification into hooks and CI so it runs automatically, not "when someone remembers."

### 8.4 Adversarial Self-Review
Use challenge prompts to break your own work before someone else does:
- _"Poke holes in this plan."_
- _"What's the edge case I'm missing?"_
- _"Prove this conclusion is correct."_
- _"Knowing what you know now, what would you do differently?"_

### 8.5 Capture Mistakes Immediately
- When an agent makes the same mistake twice, the rule belongs in the constitution, the relevant skill, or the project notes — not in someone's head.
- Update documentation **in the same PR** that fixes the mistake. A fix without a captured lesson will recur.
- Prune stale rules. An over-stuffed constitution gets ignored.

### 8.6 Scope and Context Hygiene
- One session, one task. Don't pile unrelated work into the same conversation or branch.
- If you've corrected the same issue twice and it's still wrong, stop. Restart with a clearer brief — don't keep patching.
- Hand off deep investigations to a focused subagent so the main thread stays clean.

### 8.7 Present Problems, Not Solutions
- Brief agents (and collaborators) with the *outcome* and the *constraints*, not a prescribed list of steps.
- Over-specifying the "how" prevents discovery of better approaches.
- The exception: when there is a hard requirement (security, compliance, API contract), state it explicitly.

### 8.8 Optimize for Total Time, Not Latency
- A wrong fast answer costs more time than a right slow answer.
- Prefer thorough planning, careful prompts, and explicit verification — even when they feel slower in the moment. Iteration cost dominates.

### 8.9 Reusable Skills Over One-Offs
- If you do the same workflow more than twice, turn it into a reusable skill, script, or MCP tool.
- Project-agnostic skills live where the whole team can find them. Project-specific ones live in the repo.
- Document the skill so the next person (or agent) can invoke it without rediscovering it.

### 8.10 Safe Autonomy
- Pre-approve safe, repeatable commands (build, test, lint, type-check) so agents can run them without friction.
- Do **not** disable safety checks wholesale to "go faster." Boundaries exist because past mistakes were expensive.
- For destructive or hard-to-reverse actions (force-push, drop table, delete branch), always confirm — even if you're sure.

---

## 9. Amending This Constitution

This document is living. Amend it through a pull request that explains:
- What is changing.
- Why the current rule no longer serves us.
- What the new rule is.

Once merged, the new rule applies to all subsequent work.
