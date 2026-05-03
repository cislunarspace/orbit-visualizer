from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from gui.orbit_config import OrbitConfig
from gui.process_manager import ProcessManager
from gui.server_config import ServerConfig
from gui.status_bar import StatusBar
from gui.tle_input import TLEInput


class MainWindow(QWidget):
    """Main application window composing all config widgets and server lifecycle."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("卫星轨道可视化器")
        self._process_manager = ProcessManager()
        self._process_manager.started.connect(self._on_server_started)
        self._process_manager.failed.connect(self._on_server_failed)
        self._process_manager.stopped.connect(self._on_server_stopped)
        self._server_running = False

        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)

        # Title label
        from PyQt6.QtWidgets import QLabel

        title = QLabel("卫星轨道可视化器")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        content_layout.addWidget(title)

        # Orbit config widget (contains both type checkboxes and param fields)
        self._orbit_config = OrbitConfig()
        content_layout.addWidget(self._orbit_config)

        # TLE input widget
        self._tle_input = TLEInput()
        content_layout.addWidget(self._tle_input)

        # Server config widget
        self._server_config = ServerConfig()
        content_layout.addWidget(self._server_config)

        # Start/Stop button
        self._start_stop_btn = QPushButton("启动服务器")
        self._start_stop_btn.clicked.connect(self._on_start_stop_clicked)
        content_layout.addWidget(self._start_stop_btn)

        content_layout.addStretch()
        scroll.setWidget(content)

        # Status bar at bottom
        self._status_bar = StatusBar()

        # Overall layout
        outer = QVBoxLayout(self)
        outer.addWidget(scroll, stretch=1)
        outer.addWidget(self._status_bar)

    def _on_start_stop_clicked(self) -> None:
        if self._server_running:
            self._stop_server()
        else:
            self._start_server()

    def _start_server(self) -> None:
        cfg = self._server_config.get_config()
        self._process_manager.start(cfg["host"], cfg["port"])
        self._status_bar.set_status("starting")
        self._start_stop_btn.setText("停止服务器")

    def _stop_server(self) -> None:
        self._process_manager.stop()
        self._server_running = False
        self._start_stop_btn.setText("启动服务器")
        self._status_bar.set_status("stopped")

    def _on_server_started(self, url: str) -> None:
        self._server_running = True
        self._start_stop_btn.setText("停止服务器")
        self._status_bar.set_status("running", url)
        QApplication.instance().openUrl(QUrl(url))

    def _on_server_failed(self, error: str) -> None:
        self._server_running = False
        self._start_stop_btn.setText("启动服务器")
        self._status_bar.set_status("failed")
        QMessageBox.critical(self, "服务器错误", error)

    def _on_server_stopped(self) -> None:
        self._server_running = False
        self._start_stop_btn.setText("启动服务器")
        self._status_bar.set_status("stopped")

    def closeEvent(self, event) -> None:
        if self._process_manager.is_running():
            self._stop_server()
        event.accept()
