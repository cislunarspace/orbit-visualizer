"""Tests for gui.main_window.MainWindow."""

from pytestqt.qtbot import QtBot

from gui.main_window import MainWindow


def test_main_window_has_all_sections(qtbot: QtBot) -> None:
    """Main window opens with all config sections visible."""
    window = MainWindow()
    qtbot.addWidget(window)
    # Verify key child widgets exist
    assert window._orbit_config is not None
    assert window._tle_input is not None
    assert window._server_config is not None
    assert window._status_bar is not None
    assert window._start_stop_btn is not None


def test_start_stop_button_label_stopped(qtbot: QtBot) -> None:
    """Start/Stop button shows '启动服务器' when server is stopped."""
    window = MainWindow()
    qtbot.addWidget(window)
    assert window._start_stop_btn.text() == "启动服务器"


def test_status_bar_stopped_initially(qtbot: QtBot) -> None:
    """Status bar shows '已停止' when window first opens."""
    window = MainWindow()
    qtbot.addWidget(window)
    assert window._status_bar._label.text() == "状态: 已停止"
