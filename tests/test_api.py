
from fastapi.testclient import TestClient

from app import app, service

client = TestClient(app)


def setup_function():
    service.devices.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_register_device():
    response = client.post(
        "/devices",
        json={
            "name": "Temperature Sensor",
            "device_type": "temperature_sensor",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Temperature Sensor"
    assert data["device_type"] == "temperature_sensor"
    assert data["last_heartbeat"] is None


def test_register_device_with_empty_name():
    response = client.post(
        "/devices",
        json={
            "name": "",
            "device_type": "temperature_sensor",
        },
    )

    assert response.status_code == 422
