from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


# ── Shared base ──────────────────────────────────────────────────────────────
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    priority: int = Field(default=1, ge=1, le=5)  # 1=low … 5=critical


# ── DB table model ────────────────────────────────────────────────────────────
class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ── Request / response schemas ────────────────────────────────────────────────
class TaskCreate(TaskBase):
    """POST /tasks — all base fields required except completed/priority (have defaults)."""
    pass


class TaskUpdate(SQLModel):
    """PUT /tasks/{id} — full replacement, all fields required."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool
    priority: int = Field(ge=1, le=5)


class TaskPatch(SQLModel):
    """PATCH /tasks/{id} — partial update, all fields optional."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)


class TaskRead(TaskBase):
    """Response schema — includes DB-generated fields."""
    id: int
    created_at: datetime
    updated_at: datetime
