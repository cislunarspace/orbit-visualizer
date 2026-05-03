from pytestqt.qtbot import QtBot

from gui.tle_input import TLEInput
from src.satellites import get_default_satellite, list_builtin_satellites


def test_builtin_satellite_catalog_drives_gui_presets(qtbot: QtBot) -> None:
    """Built-in satellites come from one catalog and populate the GUI preset flow."""
    satellites = list_builtin_satellites()
    assert [sat.name for sat in satellites] == ["ISS", "Hubble", "Starlink-1452"]
    assert get_default_satellite() == satellites[0]

    widget = TLEInput()
    qtbot.addWidget(widget)

    widget._preset.setCurrentText(get_default_satellite().name)
    assert widget.get_tle() == (
        get_default_satellite().tle_line1,
        get_default_satellite().tle_line2,
    )
