"""Tests for gui.status_bar.StatusBar."""

from pytestqt.qtbot import QtBot

from gui.status_bar import StatusBar


def test_status_bar_stopped_shows_correct_label(qtbot: QtBot) -> None:
    """Status bar shows '状态: 已停止' when stopped."""
    widget = StatusBar()
    qtbot.addWidget(widget)
    widget.set_status("stopped")
    assert widget._label.text() == "状态: 已停止"
    assert not widget._link.isVisible()


def test_status_bar_starting_shows_correct_label(qtbot: QtBot) -> None:
    """Status bar shows '状态: 启动中...' when starting."""
    widget = StatusBar()
    qtbot.addWidget(widget)
    widget.set_status("starting")
    assert widget._label.text() == "状态: 启动中..."


def test_status_bar_running_shows_label_and_link(qtbot: QtBot) -> None:
    """Status bar shows '状态: 运行中' with browser link when running."""
    widget = StatusBar()
    qtbot.addWidget(widget)
    widget.show()
    widget.set_status("running", "http://127.0.0.1:8000")
    qtbot.waitExposed(widget)
    assert widget._label.text() == "状态: 运行中"
    assert widget._link.isVisible()
    assert "打开浏览器" in widget._link.text()


def test_status_bar_failed_shows_correct_label(qtbot: QtBot) -> None:
    """Status bar shows '状态: 启动失败' when failed."""
    widget = StatusBar()
    qtbot.addWidget(widget)
    widget.set_status("failed")
    assert widget._label.text() == "状态: 启动失败"
    assert not widget._link.isVisible()
