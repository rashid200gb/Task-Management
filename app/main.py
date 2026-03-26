"""
Task Management API
- FastAPI + SQLModel
- Neon (PostgreSQL) in production, SQLite fallback locally
- Full CRUD: Create, List, Get, Update (full), Patch (partial), Delete
"""
from contextlib import asynccontextmanager
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session

from .database import create_db_and_tables, get_session
from .models import TaskCreate, TaskPatch, TaskRead, TaskUpdate
from . import crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Task Management API",
    description="AI-Native Task Manager — backend API with Neon PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

SessionDep = Annotated[Session, Depends(get_session)]


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


# ── Tasks ─────────────────────────────────────────────────────────────────────
@app.get("/tasks", response_model=list[TaskRead], tags=["tasks"])
def list_tasks(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    completed: Optional[bool] = Query(default=None),
):
    """List tasks with optional filtering by completion status."""
    return crud.list_tasks(session, offset=offset, limit=limit, completed=completed)


@app.get("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def get_task(task_id: int, session: SessionDep):
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=TaskRead, status_code=201, tags=["tasks"])
def create_task(data: TaskCreate, session: SessionDep):
    return crud.create_task(session, data)


@app.put("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def update_task(task_id: int, data: TaskUpdate, session: SessionDep):
    """Full replacement — all fields required."""
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(session, task, data)


@app.patch("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def patch_task(task_id: int, data: TaskPatch, session: SessionDep):
    """Partial update — send only fields you want to change."""
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.patch_task(session, task, data)


@app.delete("/tasks/{task_id}", status_code=204, tags=["tasks"])
def delete_task(task_id: int, session: SessionDep):
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(session, task)
