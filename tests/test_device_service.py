from device_service import DeviceService


def test_register_device():
    service = DeviceService()

    device = service.register_device(
        name="Temperature Sensor",
        device_type="temperature_sensor",
    )

    assert device["name"] == "Temperature Sensor"
    assert device["device_type"] == "temperature_sensor"
    assert device["id"]
    assert device["last_heartbeat"] is None


def test_register_device_with_empty_name():
    service = DeviceService()

    try:
        service.register_device(
            name="   ",
            device_type="temperature_sensor",
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Device name cannot be empty"


def test_record_heartbeat():
    service = DeviceService()

    device = service.register_device(
        name="Sensor A",
        device_type="temperature_sensor",
    )

    updated_device = service.record_heartbeat(device["id"])

    assert updated_device["last_heartbeat"] is not None


def test_unknown_device_heartbeat():
    service = DeviceService()

    try:
        service.record_heartbeat("unknown-id")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Device not found"



def test_device_status():
    service = DeviceService()

    device = service.register_device(
        name="Sensor B",
        device_type="temperature_sensor",
    )

    assert service.get_device_status(device["id"]) == "OFFLINE"

    service.record_heartbeat(device["id"])

    assert service.get_device_status(device["id"]) == "ONLINE"
