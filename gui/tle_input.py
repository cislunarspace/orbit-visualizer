from PyQt6.QtWidgets import QComboBox, QFormLayout, QGroupBox, QLineEdit, QVBoxLayout, QWidget

# TLE presets keyed by satellite name
TLE_PRESETS: dict[str, tuple[str, str]] = {
    "ISS": (
        "1 25544U 98067A   25123.56789017  .00000012  00000-0  12345-6 0  1234",
        "2 25544  51.6400  10.0000 0001234  10.0000  350.0000 15.48999999123456",
    ),
    "Hubble": (
        "1 20580U 90039B   25123.50000000  .00000000  00000-0  00000-0 0  9999",
        "2 20580  28.4700 325.0000 0001234  10.0000 200.0000 15.48999999123456",
    ),
    "Starlink-1452": (
        "1 44083U 19029Q   25123.50000000  .00000000  00000-0  00000-0 0  9999",
        "2 44083  53.0000  10.0000 0001234  10.0000 350.0000 15.50000000123456",
    ),
}


class TLEInput(QWidget):
    """TLE preset selector and free-text TLE input fields."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        group = QGroupBox("TLE 输入")
        form = QFormLayout()

        self._preset = QComboBox()
        self._preset.addItems(["ISS", "Hubble", "Starlink-1452", "Custom"])
        self._preset.setCurrentText("ISS")
        self._preset.currentTextChanged.connect(self._on_preset_changed)

        self._line1 = QLineEdit()
        self._line1.setPlaceholderText("TLE Line 1")
        self._line2 = QLineEdit()
        self._line2.setPlaceholderText("TLE Line 2")

        # Populate with ISS preset initially
        self._populate_preset("ISS")

        form.addRow("卫星:", self._preset)
        form.addRow("TLE Line 1:", self._line1)
        form.addRow("TLE Line 2:", self._line2)
        group.setLayout(form)
        layout.addWidget(group)

    def _populate_preset(self, name: str) -> None:
        if name in TLE_PRESETS:
            line1, line2 = TLE_PRESETS[name]
            self._line1.setText(line1)
            self._line2.setText(line2)
        elif name == "Custom":
            self._line1.clear()
            self._line2.clear()

    def _on_preset_changed(self, text: str) -> None:
        self._populate_preset(text)

    def get_tle(self) -> tuple[str, str]:
        """Return (line1, line2) current values."""
        return self._line1.text(), self._line2.text()
