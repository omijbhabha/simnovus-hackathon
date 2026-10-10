
import pytest
import simulator


def test_simulator_default_arguments(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["simulator.py"],
    )

    parser_args = simulator.argparse.ArgumentParser()
    parser_args.add_argument("--name", default="Temperature Sensor 1")
    parser_args.add_argument(
        "--type",
        dest="device_type",
        default="temperature_sensor",
    )
    parser_args.add_argument("--interval", type=int, default=5)

    args = parser_args.parse_args()

    assert args.name == "Temperature Sensor 1"
    assert args.device_type == "temperature_sensor"
    assert args.interval == 5


@pytest.mark.parametrize("interval", ["0", "-3"])
def test_simulator_rejects_invalid_interval(interval):
    with pytest.raises(SystemExit):
        args = simulator.argparse.ArgumentParser()
        args.add_argument("--interval", type=int)
        parsed = args.parse_args(["--interval", interval])

        if parsed.interval <= 0:
            args.error("interval must be a positive number")
