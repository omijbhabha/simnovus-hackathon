
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



def test_list_devices():
    client.post(
        "/devices",
        json={
            "name": "Sensor A",
            "device_type": "temperature_sensor",
        },
    )

    response = client.get("/devices")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Sensor A"


def test_summary_endpoint():
    response = client.get("/summary")

    assert response.status_code == 200
    assert response.json() == {
        "total_devices": 0,
        "online_devices": 0,
        "offline_devices": 0,
    }


def test_device_heartbeat():
    registration = client.post(
        "/devices",
        json={
            "name": "Heartbeat Sensor",
            "device_type": "temperature_sensor",
        },
    )

    device_id = registration.json()["id"]

    response = client.post(
        f"/devices/{device_id}/heartbeat"
    )

    assert response.status_code == 200
    assert response.json()["id"] == device_id
    assert response.json()["last_heartbeat"] is not None


def test_heartbeat_for_unknown_device():
    response = client.post(
        "/devices/unknown-id/heartbeat"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_device_status_endpoint():
    registration = client.post(
        "/devices",
        json={
            "name": "Status Sensor",
            "device_type": "temperature_sensor",
        },
    )

    device_id = registration.json()["id"]

    # A device without a heartbeat should be offline.
    response = client.get(f"/devices/{device_id}/status")

    assert response.status_code == 200
    assert response.json() == {
        "device_id": device_id,
        "status": "OFFLINE",
    }

    # After a heartbeat, the device should be online.
    client.post(f"/devices/{device_id}/heartbeat")

    response = client.get(f"/devices/{device_id}/status")

    assert response.status_code == 200
    assert response.json() == {
        "device_id": device_id,
        "status": "ONLINE",
    }
