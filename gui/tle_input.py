from PyQt6.QtWidgets import QComboBox, QFormLayout, QGroupBox, QLineEdit, QVBoxLayout, QWidget

from src.satellites import Satellite, get_default_satellite, get_satellite, list_builtin_satellites


class TLEInput(QWidget):
    """TLE preset selector and free-text TLE input fields."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        group = QGroupBox("TLE 输入")
        form = QFormLayout()

        self._preset = QComboBox()
        self._preset.addItems([sat.name for sat in list_builtin_satellites()] + ["Custom"])
        self._preset.setCurrentText(get_default_satellite().name)
        self._preset.currentTextChanged.connect(self._on_preset_changed)

        self._line1 = QLineEdit()
        self._line1.setPlaceholderText("TLE Line 1")
        self._line2 = QLineEdit()
        self._line2.setPlaceholderText("TLE Line 2")

        self._populate_preset(get_default_satellite().name)

        form.addRow("卫星:", self._preset)
        form.addRow("TLE Line 1:", self._line1)
        form.addRow("TLE Line 2:", self._line2)
        group.setLayout(form)
        layout.addWidget(group)

    def _populate_preset(self, name: str) -> None:
        if name == "Custom":
            self._line1.clear()
            self._line2.clear()
            return
        satellite = get_satellite(name)
        self._line1.setText(satellite.tle_line1)
        self._line2.setText(satellite.tle_line2)

    def _on_preset_changed(self, text: str) -> None:
        self._populate_preset(text)

    def get_tle(self) -> tuple[str, str]:
        """Return (line1, line2) current values."""
        return self._line1.text(), self._line2.text()

    def get_satellite(self) -> Satellite:
        """Return the selected built-in or custom satellite."""
        name = self._preset.currentText()
        if name == "Custom":
            return Satellite(name="Custom", tle_line1=self._line1.text(), tle_line2=self._line2.text())
        return get_satellite(name)
