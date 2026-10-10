import pytest
from fastapi.testclient import TestClient
import simulator


client = TestClient(simulator.control_app)


@pytest.fixture(autouse=True)
def reset_devices():
    simulator.devices.clear()
    simulator.devices.update({
        "device-01": {
            "id": "test-device-01",
            "active": True,
            "next_heartbeat": 0,
        },
        "device-03": {
            "id": "test-device-03",
            "active": True,
            "next_heartbeat": 0,
        },
    })
    yield
    simulator.devices.clear()


def test_list_simulated_devices():
    response = client.get("/simulator/devices")

    assert response.status_code == 200
    assert response.json()["device-01"]["active"] is True


def test_stop_device():
    response = client.post("/simulator/devices/device-03/stop")

    assert response.status_code == 200
    assert simulator.devices["device-03"]["active"] is False


def test_start_device():
    simulator.devices["device-03"]["active"] = False

    response = client.post("/simulator/devices/device-03/start")

    assert response.status_code == 200
    assert simulator.devices["device-03"]["active"] is True


def test_stop_unknown_device():
    response = client.post("/simulator/devices/unknown/stop")

    assert response.status_code == 404


def test_start_unknown_device():
    response = client.post("/simulator/devices/unknown/start")

    assert response.status_code == 404
