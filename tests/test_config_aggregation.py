"""End-to-end config aggregation tests."""

from pytestqt.qtbot import QtBot

from gui.orbit_config import OrbitConfig
from gui.server_config import ServerConfig
from gui.tle_input import TLEInput


def test_orbit_config_returns_correct_dict_structure(qtbot: QtBot) -> None:
    """OrbitConfig.get_config() returns expected structure with correct types."""
    widget = OrbitConfig()
    qtbot.addWidget(widget)
    cfg = widget.get_config()
    assert isinstance(cfg["types"], list)
    assert isinstance(cfg["hours"], int)
    assert isinstance(cfg["step"], int)
    assert isinstance(cfg["base_time"], __import__("datetime").datetime)
    assert isinstance(cfg["r0"], float)
    assert cfg["hours"] == 24


def test_server_config_returns_correct_dict_structure(qtbot: QtBot) -> None:
    """ServerConfig.get_config() returns custom host and port."""
    widget = ServerConfig()
    qtbot.addWidget(widget)
    widget._host.setText("0.0.0.0")
    widget._port.setValue(9000)
    cfg = widget.get_config()
    assert cfg["host"] == "0.0.0.0"
    assert cfg["port"] == 9000
