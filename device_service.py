
from datetime import datetime, timezone
from uuid import uuid4


class DeviceService:
    def __init__(self):
        self.devices = {}

    def register_device(self, name: str, device_type: str) -> dict:
        name = name.strip()
        device_type = device_type.strip()

        if not name:
            raise ValueError("Device name cannot be empty")

        if not device_type:
            raise ValueError("Device type cannot be empty")

        device = {
            "id": str(uuid4()),
            "name": name,
            "device_type": device_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_heartbeat": None,
        }

        self.devices[device["id"]] = device
        return device

    def record_heartbeat(self, device_id: str) -> dict:
        if device_id not in self.devices:
            raise ValueError("Device not found")

        self.devices[device_id]["last_heartbeat"] = (
            datetime.now(timezone.utc).isoformat()
        )

        return self.devices[device_id]

    def list_devices(self) -> list:
        return list(self.devices.values())

    def get_device(self, device_id: str) -> dict:
        if device_id not in self.devices:
            raise ValueError("Device not found")

        return self.devices[device_id]