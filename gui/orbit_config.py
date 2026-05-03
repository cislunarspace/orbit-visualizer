from datetime import datetime, timezone

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDateTimeEdit,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.orbit.request import OrbitRequest
from src.satellites import Satellite


class OrbitConfig(QWidget):
    """Orbit type checkboxes and global orbit parameters."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        # Orbit type checkboxes
        type_group = QGroupBox("轨道类型")
        type_layout = QVBoxLayout()
        self._cb_state_vector = QCheckBox("状态向量 (state_vector)")
        self._cb_state_vector.setChecked(True)
        self._cb_tle = QCheckBox("TLE (tle)")
        self._cb_tle.setChecked(True)
        self._cb_broadcast = QCheckBox("广播星历 (broadcast)")
        self._cb_broadcast.setChecked(True)
        self._cb_precise = QCheckBox("精密星历 (precise)")
        self._cb_precise.setChecked(True)
        type_layout.addWidget(self._cb_state_vector)
        type_layout.addWidget(self._cb_tle)
        type_layout.addWidget(self._cb_broadcast)
        type_layout.addWidget(self._cb_precise)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # Orbit parameters
        param_group = QGroupBox("轨道参数")
        param_layout = QFormLayout()

        self._hours = QSpinBox()
        self._hours.setRange(1, 168)
        self._hours.setValue(24)
        self._hours.setSuffix(" 小时")

        self._step = QSpinBox()
        self._step.setRange(1, 3600)
        self._step.setValue(60)
        self._step.setSuffix(" 秒")

        self._base_time = QDateTimeEdit()
        self._base_time.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self._base_time.setDateTime(datetime.now(timezone.utc))
        self._base_time.setTimeSpec(Qt.TimeSpec.UTC)

        self._r0 = QDoubleSpinBox()
        self._r0.setRange(6e6, 10e7)
        self._r0.setValue(7_000_000.0)
        self._r0.setSuffix(" m")
        self._r0.setDecimals(0)

        param_layout.addRow("投影时长:", self._hours)
        param_layout.addRow("时间步长:", self._step)
        param_layout.addRow("起始时间:", self._base_time)
        param_layout.addRow("轨道半径:", self._r0)
        param_group.setLayout(param_layout)
        layout.addWidget(param_group)
        layout.addStretch()

    def get_config(self) -> dict:
        """Return current orbit configuration."""
        request = self.get_orbit_request()
        return {
            "types": list(request.types),
            "hours": request.hours,
            "step": request.step,
            "base_time": request.base_time,
            "r0": request.radius_m,
        }

    def get_orbit_request(self, satellite: Satellite | None = None) -> OrbitRequest:
        """Return current orbit configuration as a domain request."""
        types = []
        if self._cb_state_vector.isChecked():
            types.append("state_vector")
        if self._cb_tle.isChecked():
            types.append("tle")
        if self._cb_broadcast.isChecked():
            types.append("broadcast")
        if self._cb_precise.isChecked():
            types.append("precise")
        base_time = (
            self._base_time.dateTime().toPyDateTime().astimezone(timezone.utc)
            if self._base_time.dateTime().toPyDateTime().tzinfo is not None
            else self._base_time.dateTime().toPyDateTime().replace(tzinfo=timezone.utc)
        )
        return OrbitRequest(
            types=tuple(types),  # type: ignore[arg-type]
            hours=self._hours.value(),
            step=self._step.value(),
            base_time=base_time,
            radius_m=self._r0.value(),
            satellite=satellite,
        )
