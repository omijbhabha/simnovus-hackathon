import time
import requests
import argparse


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
    parser = argparse.ArgumentParser(
        description="Simulate a device sending heartbeats"
    )

    parser.add_argument(
        "--name",
        default="Temperature Sensor 1",
        help="Name of the device",
    )
    parser.add_argument(
        "--type",
        dest="device_type",
        default="temperature_sensor",
        help="Type of the device",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Heartbeat interval in seconds",
    )

    args = parser.parse_args()

    try:
        simulate_device(
            name=args.name,
            device_type=args.device_type,
            interval=args.interval,
        )
    except requests.RequestException as exc:
        print(f"Simulator API error: {exc}")