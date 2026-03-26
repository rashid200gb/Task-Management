"""
Task CRUD tests — cover happy paths, edge cases, and validation.
All tests run against an in-memory SQLite DB (see conftest.py).
"""
import pytest
from fastapi.testclient import TestClient


# ── Helpers ───────────────────────────────────────────────────────────────────
def _create(client: TestClient, **kwargs) -> dict:
    payload = {"title": "Test task", "priority": 1, **kwargs}
    resp = client.post("/tasks", json=payload)
    assert resp.status_code == 201
    return resp.json()


# ── Create ────────────────────────────────────────────────────────────────────
class TestCreateTask:
    def test_create_minimal(self, client: TestClient):
        resp = client.post("/tasks", json={"title": "Buy milk"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Buy milk"
        assert data["completed"] is False
        assert data["priority"] == 1
        assert "id" in data
        assert "created_at" in data

    def test_create_full(self, client: TestClient):
        payload = {
            "title": "Write report",
            "description": "Q1 financials",
            "completed": False,
            "priority": 4,
        }
        resp = client.post("/tasks", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["description"] == "Q1 financials"
        assert data["priority"] == 4

    def test_create_empty_title_rejected(self, client: TestClient):
        resp = client.post("/tasks", json={"title": ""})
        assert resp.status_code == 422

    def test_create_priority_out_of_range(self, client: TestClient):
        resp = client.post("/tasks", json={"title": "X", "priority": 6})
        assert resp.status_code == 422

    def test_create_missing_title(self, client: TestClient):
        resp = client.post("/tasks", json={"description": "no title"})
        assert resp.status_code == 422


# ── Read ──────────────────────────────────────────────────────────────────────
class TestReadTask:
    def test_list_empty(self, client: TestClient):
        resp = client.get("/tasks")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_all(self, client: TestClient):
        _create(client, title="Task A")
        _create(client, title="Task B")
        resp = client.get("/tasks")
        assert len(resp.json()) == 2

    def test_list_filter_completed(self, client: TestClient):
        _create(client, title="Done", completed=True)
        _create(client, title="Pending", completed=False)
        resp = client.get("/tasks?completed=true")
        assert resp.status_code == 200
        items = resp.json()
        assert len(items) == 1
        assert items[0]["title"] == "Done"

    def test_list_filter_pending(self, client: TestClient):
        _create(client, title="Done", completed=True)
        _create(client, title="Pending", completed=False)
        resp = client.get("/tasks?completed=false")
        assert len(resp.json()) == 1

    def test_list_pagination(self, client: TestClient):
        for i in range(5):
            _create(client, title=f"Task {i}")
        resp = client.get("/tasks?offset=2&limit=2")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_get_by_id(self, client: TestClient):
        task = _create(client, title="Specific task")
        resp = client.get(f"/tasks/{task['id']}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Specific task"

    def test_get_not_found(self, client: TestClient):
        resp = client.get("/tasks/9999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Task not found"


# ── Update (full) ─────────────────────────────────────────────────────────────
class TestUpdateTask:
    def test_put_updates_all_fields(self, client: TestClient):
        task = _create(client, title="Old title", priority=1)
        payload = {
            "title": "New title",
            "description": "Updated desc",
            "completed": True,
            "priority": 5,
        }
        resp = client.put(f"/tasks/{task['id']}", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "New title"
        assert data["completed"] is True
        assert data["priority"] == 5

    def test_put_not_found(self, client: TestClient):
        resp = client.put("/tasks/9999", json={
            "title": "X", "completed": False, "priority": 1
        })
        assert resp.status_code == 404

    def test_put_updates_updated_at(self, client: TestClient):
        task = _create(client)
        original_ts = task["updated_at"]
        import time; time.sleep(0.01)
        resp = client.put(f"/tasks/{task['id']}", json={
            "title": "Changed", "completed": True, "priority": 3
        })
        assert resp.json()["updated_at"] >= original_ts


# ── Patch (partial) ───────────────────────────────────────────────────────────
class TestPatchTask:
    def test_patch_title_only(self, client: TestClient):
        task = _create(client, title="Original", priority=2)
        resp = client.patch(f"/tasks/{task['id']}", json={"title": "Patched"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Patched"
        assert data["priority"] == 2  # unchanged

    def test_patch_completed(self, client: TestClient):
        task = _create(client, completed=False)
        resp = client.patch(f"/tasks/{task['id']}", json={"completed": True})
        assert resp.json()["completed"] is True

    def test_patch_empty_body_no_change(self, client: TestClient):
        task = _create(client, title="Stable")
        resp = client.patch(f"/tasks/{task['id']}", json={})
        assert resp.status_code == 200
        assert resp.json()["title"] == "Stable"

    def test_patch_not_found(self, client: TestClient):
        resp = client.patch("/tasks/9999", json={"title": "X"})
        assert resp.status_code == 404


# ── Delete ────────────────────────────────────────────────────────────────────
class TestDeleteTask:
    def test_delete_existing(self, client: TestClient):
        task = _create(client)
        resp = client.delete(f"/tasks/{task['id']}")
        assert resp.status_code == 204

    def test_deleted_task_not_found(self, client: TestClient):
        task = _create(client)
        client.delete(f"/tasks/{task['id']}")
        resp = client.get(f"/tasks/{task['id']}")
        assert resp.status_code == 404

    def test_delete_not_found(self, client: TestClient):
        resp = client.delete("/tasks/9999")
        assert resp.status_code == 404

    def test_delete_reduces_list(self, client: TestClient):
        t1 = _create(client, title="Keep")
        t2 = _create(client, title="Delete me")
        client.delete(f"/tasks/{t2['id']}")
        tasks = client.get("/tasks").json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Keep"
