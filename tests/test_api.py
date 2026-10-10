
from fastapi.testclient import TestClient

from app import app, service

client = TestClient(app)


def setup_function():
    service.devices.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
