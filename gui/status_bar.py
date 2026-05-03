from typing import Literal

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QLabel, QPushButton, QStatusBar

from PyQt6.QtGui import QDesktopServices


class StatusBar(QStatusBar):
    """
    Displays server status and an optional browser hyperlink.

    States:
        stopped  — "状态: 已停止"
        starting — "状态: 启动中..."
        running  — "状态: 运行中" + clickable browser link
        failed   — "状态: 启动失败"
    """

    def __init__(self) -> None:
        super().__init__()
        self._label = QLabel("状态: 已停止")
        self._link = QPushButton("打开浏览器 →")
        self._link.setVisible(False)
        self._link.clicked.connect(self._open_browser)
        self._current_url: str = ""

        self.addWidget(self._label)
        self.addPermanentWidget(self._link)

    def set_status(self, state: Literal["stopped", "starting", "running", "failed"], url: str = "") -> None:
        """Update the status label and optionally show the browser link."""
        self._current_url = url
        if state == "stopped":
            self._label.setText("状态: 已停止")
            self._link.setVisible(False)
        elif state == "starting":
            self._label.setText("状态: 启动中...")
            self._link.setVisible(False)
        elif state == "running":
            self._label.setText("状态: 运行中")
            self._link.setVisible(True)
        elif state == "failed":
            self._label.setText("状态: 启动失败")
            self._link.setVisible(False)

    def _open_browser(self) -> None:
        if self._current_url:
            QDesktopServices.openUrl(QUrl(self._current_url))
