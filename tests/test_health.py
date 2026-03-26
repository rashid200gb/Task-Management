"""Health endpoint tests."""
from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_not_found(client: TestClient):
    """No root route — confirms we haven't added accidental catch-all."""
    response = client.get("/")
    assert response.status_code == 404
