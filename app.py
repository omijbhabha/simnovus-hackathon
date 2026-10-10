from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from device_service import DeviceService

app = FastAPI(
    title="Simnovus Device Fleet Monitor",
    description="A simple API for monitoring device heartbeats and fleet status.",
    version="1.0.0",
)

service = DeviceService()


class DeviceRegistration(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    device_type: str = Field(min_length=1, max_length=100)

@app.get("/")
def home():
    return {
        "message": "Simnovus Device Fleet Monitor is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/devices", status_code=201)
def register_device(request: DeviceRegistration):
    try:
        return service.register_device(
            name=request.name,
            device_type=request.device_type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/devices/{device_id}/heartbeat")
def send_heartbeat(device_id: str):
    try:
        return service.record_heartbeat(device_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

@app.get("/devices")
def list_devices():
    return service.list_devices()

@app.get("/devices/{device_id}")
def get_device(device_id: str):
    try:
        return service.get_device(device_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@app.get("/devices/{device_id}/status")
def get_device_status(device_id: str):
    try:
        return {
            "device_id": device_id,
            "status": service.get_device_status(device_id),
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@app.get("/summary")
def get_summary():
    return service.get_summary()
