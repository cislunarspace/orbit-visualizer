# Development Guide | 开发指南

**English** | [中文](#中文开发指南)

## Development Environment Setup

```bash
# Clone and install
git clone https://github.com/cislunarspace/orbit-visualizer.git
cd orbit-visualizer
uv sync

# Run tests
uv run pytest

# Launch GUI (development)
uv run python -m gui

# Launch server directly (development)
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

## Adding a New Orbit Type

This guide adds a new orbit type: **GEO (Geostationary Orbit)**.

### Step 1: Add the generation function in `main.py`

Add a new function:

```python
def generate_geo_orbit(hours: int = 24, step: int = 60, base_time: datetime | None = None) -> list[dict]:
    """Simulated geostationary orbit at 35,786 km altitude."""
    t0 = base_time or datetime.now(timezone.utc)
    a = 42_164_000  # GEO semi-major axis in meters
    data = []
    for i in range(0, hours * 3600, step):
        theta = 2 * np.pi * i / (hours * 3600)
        x = a * np.cos(theta)
        y = a * np.sin(theta)
        z = 0.0
        t = t0 + timedelta(seconds=i)
        data.append({"time": _utc_str(t), "pos": [x, y, z]})
    return data
```

### Step 2: Add the API endpoint

Add a new route in `main.py`:

```python
@app.get("/api/orbit/geo")
def orbit_geo() -> list[dict]:
    data = generate_geo_orbit()
    return make_czml("地球静止轨道(GEO)", data, [255, 128, 0, 180])
```

### Step 3: Update `GET /api/all`

Update the `all_orbits` endpoint to handle the new type:

```python
@app.get("/api/all")
def all_orbits(types: str | None = None) -> list[dict]:
    t0 = datetime.now(timezone.utc)
    sat = get_default_satellite()
    requested = set(types.split(",")) if types else None

    czml: list[dict] = []

    if requested is None or "state_vector" in requested:
        sv = generate_state_vector_orbit(base_time=t0)
        czml.append(make_czml("状态向量", sv, [0, 255, 255, 180])[1])

    if requested is None or "tle" in requested:
        tle = tle_to_orbit(sat.tle_line1, sat.tle_line2, base_time=t0)
        czml.append(make_czml("TLE", tle, [255, 255, 0, 180])[1])

    if requested is None or "broadcast" in requested:
        brd = generate_broadcast_ephemeris(base_time=t0)
        czml.append(make_czml("广播星历", brd, [0, 255, 0, 180])[1])

    if requested is None or "precise" in requested:
        pre = generate_precise_ephemeris(base_time=t0)
        czml.append(make_czml("精密星历", pre, [255, 0, 0, 180])[1])

    # NEW
    if requested is None or "geo" in requested:
        geo = generate_geo_orbit(base_time=t0)
        czml.append(make_czml("GEO", geo, [255, 128, 0, 180])[1])

    return [{"id": "document", "version": "1.0"}, *czml]
```

### Step 4: Add the checkbox to the GUI

Edit `gui/orbit_config.py`:

```python
self._cb_geo = QCheckBox("地球静止轨道 (geo)")
self._cb_geo.setChecked(True)
type_layout.addWidget(self._cb_geo)
```

And update `get_config()`:

```python
if self._cb_geo.isChecked():
    types.append("geo")
```

### Step 5: Add a test

Add to `tests/test_orbit_filter.py`:

```python
def test_api_all_filter_geo():
    response = client.get("/api/all?types=geo")
    packets = response.json()
    ids = [p.get("id") for p in packets]
    assert "document" in ids
    assert "GEO" in ids
    # Only GEO, no others
    non_doc = [p["id"] for p in packets if p["id"] != "document"]
    assert non_doc == ["GEO"]
```

---

## Adding a New TLE Satellite

### Step 1: Update `src/satellites/tle_data.py`

Add a new TLE constant:

```python
_GALILEO_TLE1 = "1 43055U 17069A   25123.50000000  .00000000  00000-0  00000-0 0  9999"
_GALILEO_TLE2 = "2 43055  56.0000  10.0000 0001234  10.0000 350.0000 15.20000000123456"
```

### Step 2: Add to the GUI preset list

Edit `gui/tle_input.py`:

```python
TLE_PRESETS: dict[str, tuple[str, str]] = {
    "ISS": (_ISS_TLE1, _ISS_TLE2),
    "Hubble": (_HST_TLE1, _HST_TLE2),
    "Starlink-1452": (_SLK_TLE1, _SLK_TLE2),
    # NEW
    "Galileo-XXX": (_GALILEO_TLE1, _GALILEO_TLE2),
    "Custom": None,
}
```

And update the combo box items:

```python
self._preset.addItems(["ISS", "Hubble", "Starlink-1452", "Galileo-XXX", "Custom"])
```

### Step 3: Add the TLE import

```python
from .tle_data import _GALILEO_TLE1, _GALILEO_TLE2
```

---

## Adding a New GUI Widget

Create a new file `gui/my_widget.py`:

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MyWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("My new widget"))

    def get_value(self) -> str:
        return "my value"
```

Then add it to `MainWindow` in `gui/main_window.py`:

```python
from gui.my_widget import MyWidget

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # ... existing code ...
        self._my_widget = MyWidget()
        content_layout.addWidget(self._my_widget)
```

---

## Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_orbit_filter.py

# Run with coverage
uv run pytest --cov=main --cov=gui --cov-report=term-missing
```

Test file naming convention:
- `tests/test_*.py` — test modules
- Use `pytest-qt` fixtures: `qtbot` for widget tests
- Use FastAPI `TestClient` for API tests

---

## Code Style

- **Python**: Follow PEP 8, use type annotations on all function signatures
- **Format**: `ruff check .` for linting, `ruff format .` for formatting (if configured)
- **PyQt6**: Use `pyqtSignal` (not `Signal`), prefer `threading.Thread` over `QThread` for subprocess management

---

## Project Dependencies

All dependencies are listed in `pyproject.toml`:

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn[standard]` | ASGI server |
| `sgp4` | SGP4 orbital propagation |
| `numpy` | Numerical computation |
| `PyQt6` | Desktop GUI framework |

Dev dependencies:

| Package | Purpose |
|---------|---------|
| `pytest` | Test framework |
| `pytest-qt` | PyQt widget testing |
| `pytest-cov` | Coverage reporting |

---

## 中文开发指南

### 开发环境设置

```bash
git clone https://github.com/cislunarspace/orbit-visualizer.git
cd orbit-visualizer
uv sync
uv run pytest
```

### 添加新轨道类型（以 GEO 为例）

**第一步**：在 `main.py` 中添加生成函数：

```python
def generate_geo_orbit(hours: int = 24, step: int = 60,
                        base_time: datetime | None = None) -> list[dict]:
    """地球静止轨道：35,786 km 高度"""
    t0 = base_time or datetime.now(timezone.utc)
    a = 42_164_000  # GEO 半长轴 (m)
    data = []
    for i in range(0, hours * 3600, step):
        theta = 2 * np.pi * i / (hours * 3600)
        x = a * np.cos(theta)
        y = a * np.sin(theta)
        z = 0.0
        t = t0 + timedelta(seconds=i)
        data.append({"time": _utc_str(t), "pos": [x, y, z]})
    return data
```

**第二步**：在 `main.py` 中添加 API 端点：

```python
@app.get("/api/orbit/geo")
def orbit_geo() -> list[dict]:
    data = generate_geo_orbit()
    return make_czml("GEO", data, [255, 128, 0, 180])
```

**第三步**：更新 `GET /api/all` 处理新的 `geo` 类型。

**第四步**：在 `gui/orbit_config.py` 中添加复选框。

**第五步**：添加测试用例。

### 添加新 TLE 卫星

在 `src/satellites/tle_data.py` 中添加新的 TLE 常量，并在 `gui/tle_input.py` 的 `TLE_PRESETS` 字典中注册。

### 添加新 GUI 控件

在 `gui/` 目录下创建新的 widget 文件，然后在 `gui/main_window.py` 的 `MainWindow.__init__` 中实例化并添加到布局。

### 运行测试

```bash
uv run pytest                    # 所有测试
uv run pytest tests/test_*.py   # 特定文件
```

### 代码风格

- Python：遵循 PEP 8，所有函数签名带类型注解
- PyQt6：使用 `pyqtSignal`（非 `Signal`），子进程管理用 `threading.Thread`（非 `QThread`）
