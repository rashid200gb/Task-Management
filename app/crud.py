"""CRUD operations — pure database logic, no HTTP concerns."""
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Session, select

from .models import Task, TaskCreate, TaskUpdate, TaskPatch


def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)


def list_tasks(
    session: Session,
    offset: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
) -> list[Task]:
    stmt = select(Task)
    if completed is not None:
        stmt = stmt.where(Task.completed == completed)
    stmt = stmt.offset(offset).limit(limit)
    return session.exec(stmt).all()


def create_task(session: Session, data: TaskCreate) -> Task:
    task = Task.model_validate(data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task: Task, data: TaskUpdate) -> Task:
    """Full replacement — all fields overwritten."""
    for field, value in data.model_dump().items():
        setattr(task, field, value)
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def patch_task(session: Session, task: Task, data: TaskPatch) -> Task:
    """Partial update — only provided fields changed."""
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    task.updated_at = datetime.now(timezone.utc)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()
