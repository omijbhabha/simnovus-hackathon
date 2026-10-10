
import time
import requests


API_URL = "http://127.0.0.1:8000"


def register_device(name, device_type):
    response = requests.post(
        f"{API_URL}/devices",
        json={
            "name": name,
            "device_type": device_type,
        },
    )
    response.raise_for_status()
    return response.json()


def send_heartbeat(device_id):
    response = requests.post(
        f"{API_URL}/devices/{device_id}/heartbeat"
    )
    response.raise_for_status()
    return response.json()


def simulate_device(name, device_type, interval=5):
    device = register_device(name, device_type)
    device_id = device["id"]

    print(f"Registered device: {device['name']}")
    print(f"Device ID: {device_id}")

    try:
        while True:
            send_heartbeat(device_id)
            print(f"Heartbeat sent for {device['name']}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nStopped simulation for {device['name']}")


if __name__ == "__main__":
    try:
        simulate_device(
            name="Temperature Sensor 1",
            device_type="temperature_sensor",
        )
    except requests.RequestException as exc:
        print(f"Simulator API error: {exc}")