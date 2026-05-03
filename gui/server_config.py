from PyQt6.QtWidgets import QFormLayout, QGroupBox, QLineEdit, QSpinBox, QVBoxLayout, QWidget


class ServerConfig(QWidget):
    """Host and port configuration for the FastAPI server."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        group = QGroupBox("服务器配置")
        form = QFormLayout()

        self._host = QLineEdit()
        self._host.setText("127.0.0.1")
        self._host.setPlaceholderText("Host")

        self._port = QSpinBox()
        self._port.setRange(1024, 65535)
        self._port.setValue(8000)
        self._port.setSuffix(" (端口)")

        form.addRow("主机:", self._host)
        form.addRow("端口:", self._port)
        group.setLayout(form)
        layout.addWidget(group)

    def get_config(self) -> dict:
        """Return {host: str, port: int}."""
        return {
            "host": self._host.text(),
            "port": self._port.value(),
        }
