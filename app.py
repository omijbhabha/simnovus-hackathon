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