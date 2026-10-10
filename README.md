# Simnovus Device Fleet Monitor

A simple Python project for monitoring a fleet of simulated devices using FastAPI. Devices send periodic heartbeats, and the backend tracks their online/offline status.

## Features

- Register devices with a name and device type
- Record device heartbeats with timestamps
- Determine whether a device is online or offline
- View registered devices and fleet summary
- Simulate five devices sending heartbeats
- Stop and resume individual devices through a control API
- Automated tests for the API, device service, and simulator

## Technologies

- Python
- FastAPI
- Uvicorn
- Requests
- Pytest

## Setup

Clone or download the project and navigate to its directory.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Backend

Start the backend API:

```bash
uvicorn app:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Run the Simulator

Open a second terminal, activate the virtual environment, and run:

```bash
python simulator.py
```

The simulator registers five devices and sends heartbeats every five seconds.

The simulator control API runs at `http://127.0.0.1:8001`.

### Simulator Controls

List simulated devices:

```bash
curl http://127.0.0.1:8001/simulator/devices
```

Stop heartbeats for a device:

```bash
curl -X POST http://127.0.0.1:8001/simulator/devices/device-03/stop
```

Resume heartbeats for a device:

```bash
curl -X POST http://127.0.0.1:8001/simulator/devices/device-03/start
```

A stopped device will be reported as offline by the backend after its last heartbeat becomes more than 30 seconds old.

## Backend API Endpoints

| Method | Endpoint                         | Description                      |
| ------ | -------------------------------- | -------------------------------- |
| GET    | `/`                              | Basic service information        |
| GET    | `/health`                        | Health check                     |
| POST   | `/devices`                       | Register a device                |
| GET    | `/devices`                       | List registered devices          |
| GET    | `/devices/{device_id}`           | Get device details               |
| POST   | `/devices/{device_id}/heartbeat` | Record a heartbeat               |
| GET    | `/devices/{device_id}/status`    | Get device online/offline status |
| GET    | `/summary`                       | Get fleet totals                 |

## Run Tests

Run the complete test suite:

```bash
pytest -v
```

The tests cover API endpoints, device service behavior, heartbeat status, fleet summaries, and simulator controls.

## Notes

- Device information is stored in memory and is lost when the backend restarts.
- The backend and simulator control API use separate ports: `8000` and `8001`.
- Start the backend before starting the simulator.
