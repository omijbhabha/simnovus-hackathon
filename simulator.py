import time
import threading
import requests
import uvicorn
from fastapi import FastAPI, HTTPException


API_URL = "http://127.0.0.1:8000"
CONTROL_API_URL = "http://127.0.0.1:8001"
HEARTBEAT_INTERVAL = 5

control_app = FastAPI()
devices = {}


def register_device(name, device_type):
    response = requests.post(
        f"{API_URL}/devices",
        json={
            "name": name,
            "device_type": device_type,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def send_heartbeat(device_id):
    response = requests.post(
        f"{API_URL}/devices/{device_id}/heartbeat",
        timeout=5,
    )
    response.raise_for_status()


@control_app.get("/simulator/devices")
def list_simulated_devices():
    return {
        name: {
            "id": device["id"],
            "active": device["active"],
        }
        for name, device in devices.items()
    }


@control_app.post("/simulator/devices/{name}/stop")
def stop_device(name: str):
    if name not in devices:
        raise HTTPException(status_code=404, detail="Device not found")

    devices[name]["active"] = False
    return {"message": f"Heartbeats stopped for {name}"}


@control_app.post("/simulator/devices/{name}/start")
def start_device(name: str):
    if name not in devices:
        raise HTTPException(status_code=404, detail="Device not found")

    devices[name]["active"] = True
    devices[name]["next_heartbeat"] = time.time()
    return {"message": f"Heartbeats resumed for {name}"}


def run_control_api():
    uvicorn.run(
        control_app,
        host="127.0.0.1",
        port=8001,
        log_level="warning",
    )


def wait_for_control_api(timeout=10):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                f"{CONTROL_API_URL}/simulator/devices",
                timeout=1,
            )
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass

        time.sleep(0.2)

    return False


def main():
    device_types = [
        "temperature_sensor",
        "humidity_sensor",
        "pressure_sensor",
        "temperature_sensor",
        "humidity_sensor",
    ]

    try:
        for i, device_type in enumerate(device_types, start=1):
            name = f"device-{i:02d}"
            device = register_device(name, device_type)

            devices[name] = {
                "id": device["id"],
                "active": True,
                "next_heartbeat": time.time(),
            }

            print(f"Registered {name}: {device['id']}")

    except requests.RequestException as exc:
        print(f"Could not register devices: {exc}")
        return

    api_thread = threading.Thread(
        target=run_control_api,
        daemon=True,
    )
    api_thread.start()

    if not wait_for_control_api():
        print("Could not start the control API on port 8001.")
        return

    print("\nFive devices are running.")
    print(f"Control API: {CONTROL_API_URL}")
    print("Heartbeats run every 5 seconds.")
    print("Use the control API to stop or start individual devices.")
    print("Press Ctrl+C to stop the simulator.")

    try:
        while True:
            now = time.time()

            for name, device in devices.items():
                if device["active"] and now >= device["next_heartbeat"]:
                    try:
                        send_heartbeat(device["id"])
                        print(f"{name} -> heartbeat")
                    except requests.RequestException as exc:
                        print(f"Heartbeat failed for {name}: {exc}")

                    device["next_heartbeat"] = (
                        time.time() + HEARTBEAT_INTERVAL
                    )

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")


if __name__ == "__main__":
    main()
