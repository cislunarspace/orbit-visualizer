"""Tests for gui config widgets: orbit_config, tle_input, server_config."""

from datetime import datetime, timezone

from pytestqt.qtbot import QtBot

from gui.orbit_config import OrbitConfig
from gui.tle_input import TLEInput
from gui.server_config import ServerConfig


# ── OrbitConfig ────────────────────────────────────────────────────────────────


def test_orbit_config_all_checkboxes_checked_by_default(qtbot: QtBot) -> None:
    """All four orbit type checkboxes are checked by default."""
    widget = OrbitConfig()
    qtbot.addWidget(widget)
    assert widget._cb_state_vector.isChecked() is True
    assert widget._cb_tle.isChecked() is True
    assert widget._cb_broadcast.isChecked() is True
    assert widget._cb_precise.isChecked() is True


def test_orbit_config_get_config_types(qtbot: QtBot) -> None:
    """get_config returns list of checked orbit type values."""
    widget = OrbitConfig()
    qtbot.addWidget(widget)
    cfg = widget.get_config()
    assert cfg["types"] == ["state_vector", "tle", "broadcast", "precise"]

    widget._cb_tle.setChecked(False)
    cfg = widget.get_config()
    assert cfg["types"] == ["state_vector", "broadcast", "precise"]


def test_orbit_config_get_config_defaults(qtbot: QtBot) -> None:
    """get_config returns correct default values for hours, step, r0."""
    widget = OrbitConfig()
    qtbot.addWidget(widget)
    cfg = widget.get_config()
    assert cfg["hours"] == 24
    assert cfg["step"] == 60
    assert cfg["r0"] == 7_000_000.0


def test_orbit_config_get_config_has_base_time(qtbot: QtBot) -> None:
    """get_config includes a datetime for base_time."""
    widget = OrbitConfig()
    qtbot.addWidget(widget)
    cfg = widget.get_config()
    assert isinstance(cfg["base_time"], datetime)


# ── TLEInput ───────────────────────────────────────────────────────────────────


def test_tle_input_preset_iss_populates_lines(qtbot: QtBot) -> None:
    """Selecting ISS preset fills line1 and line2."""
    widget = TLEInput()
    qtbot.addWidget(widget)
    widget._preset.setCurrentText("ISS")
    line1, line2 = widget.get_tle()
    assert "25544" in line1
    assert "25544" in line2


def test_tle_input_preset_starlink_populates_lines(qtbot: QtBot) -> None:
    """Selecting Starlink preset fills line1 and line2."""
    widget = TLEInput()
    qtbot.addWidget(widget)
    widget._preset.setCurrentText("Starlink-1452")
    line1, line2 = widget.get_tle()
    assert "44083" in line1
    assert "44083" in line2


def test_tle_input_preset_custom_clears_lines(qtbot: QtBot) -> None:
    """Switching to Custom clears both fields."""
    widget = TLEInput()
    qtbot.addWidget(widget)
    widget._preset.setCurrentText("ISS")
    assert widget._line1.text() != ""
    widget._preset.setCurrentText("Custom")
    assert widget._line1.text() == ""
    assert widget._line2.text() == ""


def test_tle_input_get_tle_returns_tuple(qtbot: QtBot) -> None:
    """get_tle returns (line1, line2) strings."""
    widget = TLEInput()
    qtbot.addWidget(widget)
    widget._line1.setText("LINE1")
    widget._line2.setText("LINE2")
    line1, line2 = widget.get_tle()
    assert line1 == "LINE1"
    assert line2 == "LINE2"


# ── ServerConfig ────────────────────────────────────────────────────────────────


def test_server_config_defaults(qtbot: QtBot) -> None:
    """Server config defaults to 127.0.0.1:8000."""
    widget = ServerConfig()
    qtbot.addWidget(widget)
    cfg = widget.get_config()
    assert cfg["host"] == "127.0.0.1"
    assert cfg["port"] == 8000


def test_server_config_custom_values(qtbot: QtBot) -> None:
    """Server config returns custom host and port."""
    widget = ServerConfig()
    qtbot.addWidget(widget)
    widget._host.setText("0.0.0.0")
    widget._port.setValue(9000)
    cfg = widget.get_config()
    assert cfg["host"] == "0.0.0.0"
    assert cfg["port"] == 9000
