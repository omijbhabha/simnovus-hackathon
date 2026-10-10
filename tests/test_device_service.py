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
