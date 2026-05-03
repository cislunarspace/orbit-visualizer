# Architecture | 系统架构

**English** | [中文](#中文系统架构)

## Overview

The project has three main components:

```
┌─────────────────────────────────────────────┐
│                 PyQt6 GUI                    │
│  (gui/) Control panel, start/stop server    │
└──────────────────┬──────────────────────────┘
                   │ subprocess
                   ▼
┌─────────────────────────────────────────────┐
│          FastAPI Backend (main.py)           │
│  Orbit computation + CZML formatting         │
│  Served on 127.0.0.1:8000                   │
└──────────────────┬──────────────────────────┘
                   │ static files
                   ▼
┌─────────────────────────────────────────────┐
│          Cesium JS Frontend                 │
│  (static/) 3D globe + time-dynamic orbits    │
└─────────────────────────────────────────────┘
```

---

## Component: FastAPI Backend

**File**: `main.py`

The FastAPI application serves three roles:

1. **Orbit Computation** — Pure mathematical models producing `OrbitPoint` sequences
2. **CZML Formatting** — Transforms `OrbitPoint` lists into Cesium-readable CZML documents
3. **HTTP API** — Thin handlers composing computation + formatting

### Key Functions

| Function | Location | Purpose |
|----------|----------|---------|
| `generate_state_vector_orbit()` | `main.py:28` | Keplerian circular orbit |
| `tle_to_orbit()` | `main.py:45` | SGP4 propagation from TLE |
| `generate_broadcast_ephemeris()` | `main.py:61` | Simulated GPS MEO orbit |
| `generate_precise_ephemeris()` | `main.py:78` | Simulated SP3-like orbit |
| `make_czml()` | `main.py:95` | Format OrbitPoint list as CZML |

### Data Flow

```
HTTP Request
    │
    ▼
GET /api/all?types=state_vector,tle
    │
    ▼
For each requested type:
    │
    ├─► generate_*_orbit() ──► list[OrbitPoint]
    │                              (time: str, pos: [x, y, z] in meters)
    │
    └─► make_czml(name, data, color) ──► list[CZML packet]
                                             (document + orbit packet)
    │
    ▼
Return: list[CZML packet] ──► JSON response
```

---

## Component: Core Computation

**Package**: `src/orbit/` and `src/satellites/`

### `src/orbit/constants.py`

Physical and orbital constants:

| Constant | Value | Unit | Description |
|----------|-------|------|-------------|
| `EARTH_GRAVITATIONAL_PARAMETER` | 3.986004418e14 | m³/s² | μ = GM |
| `LEO_ORBITAL_RADIUS_M` | 7,000,000 | m | ~LEO altitude reference |
| `GPS_SEMI_MAJOR_AXIS_M` | 26,560,000 | m | GPS MEO orbit |
| `PRECISE_SEMI_MAJOR_AXIS_M` | 30,000,000 | m | Precise orbit reference |

### `src/satellites/`

| File | Purpose |
|------|---------|
| `iss.py` | `Satellite` dataclass and `get_default_satellite()` |
| `tle_data.py` | Raw TLE strings for ISS (internal use) |

### `Satellite` Domain Object

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Satellite:
    name: str
    tle_line1: str
    tle_line2: str
```

---

## Component: PyQt6 GUI

**Package**: `gui/`

| File | Responsibility |
|------|----------------|
| `main_window.py` | Composes all widgets, wires ProcessManager signals, handles window lifecycle |
| `orbit_config.py` | Orbit type checkboxes + param fields (hours, step, base_time, r0) |
| `tle_input.py` | TLE preset selector (ISS/Hubble/Starlink/Custom) + line1/line2 fields |
| `server_config.py` | Host + port fields |
| `status_bar.py` | Status display with conditional browser link |
| `process_manager.py` | Manages uvicorn subprocess lifecycle with Qt signals |
| `__main__.py` | Entry point for `python -m gui` |

### ProcessManager State Machine

```
[None] ──start()──► [Starting]
                           │
                    "Uvicorn running on" ──► [Running]
                           │                       │
                      stop()                   stop()
                           │                       │
                           ▼                       ▼
                      [Stopped] ◄───────── [Stopped]
                           │
                      (unexpected exit)
                           │
                           ▼
                       [Failed]
```

### Signals

| Signal | Emitted When |
|--------|-------------|
| `started(url)` | Server process emits "Uvicorn running on" |
| `stopped()` | Server exits cleanly after `stop()` |
| `failed(msg)` | Server exits unexpectedly with non-zero code |
| `output(line)` | Each stdout/stderr line from the server process |

---

## Component: Frontend

**Directory**: `static/`

| File | Purpose |
|------|---------|
| `index.html` | Cesium JS viewer, loads CZML from API |
| (other assets) | Cesium JS core + CDN-loaded assets |

### Data Loading Flow

```
Cesium viewer starts
    │
    ▼
GET /api/all?types=state_vector,tle,broadcast,precise
    │
    ▼
CZML JSON response
    │
    ▼
Cesium.process开放的CZMLstream
    │
    ▼
Orbit paths + satellite points rendered on 3D globe
```

---

## Key Design Decisions

### 1. GUI Starts Server as Subprocess

The GUI does not call the API over HTTP. Instead, it spawns `uvicorn main:app` as a subprocess and communicates via stdout/stderr parsing. This avoids port conflicts with an already-running server and simplifies deployment.

### 2. CZML over Raw JSON

All orbit data is formatted as CZML (Cesium Language) rather than raw JSON. This is because Cesium JS natively understands CZML for time-dynamic 3D scenes, including clock synchronization, path materials, and point styles.

### 3. SGP4 via `sgp4` Library

Rather than implementing SGP4 from scratch, the project uses the `sgp4` library (`sgp4.api.Satrec.twoline2rv`), which is the standard reference implementation maintained by the US Space Force.

### 4. Threading over QThread for Subprocess

`ProcessManager` uses `threading.Thread` (not `QThread`) to read subprocess stdout. This was chosen because `QThread` caused issues with pytest on Windows. The subprocess reader thread emits Qt signals via `pyqtSignal`, which is thread-safe.

---

## Directory Structure

```
orbit-visualizer/
├── main.py                    # FastAPI app + orbit generation
├── pyproject.toml             # Project metadata + dependencies
├── gui/
│   ├── __init__.py
│   ├── __main__.py            # Entry: python -m gui
│   ├── main_window.py         # MainWindow widget
│   ├── orbit_config.py        # OrbitConfig widget
│   ├── tle_input.py           # TLEInput widget
│   ├── server_config.py       # ServerConfig widget
│   ├── status_bar.py          # StatusBar widget
│   └── process_manager.py     # ProcessManager (QObject)
├── src/
│   ├── orbit/
│   │   ├── __init__.py
│   │   └── constants.py       # Orbital constants
│   └── satellites/
│       ├── __init__.py
│       ├── iss.py             # Satellite domain object
│       └── tle_data.py        # Raw TLE strings
├── static/
│   └── index.html             # Cesium viewer
└── tests/                     # 31 test cases
```

---

## 中文系统架构

### 概览

项目包含三个主要组件：

```
┌─────────────────────────────────────────────┐
│                 PyQt6 GUI                    │
│  (gui/) 控制面板，启动/停止服务器              │
└──────────────────┬──────────────────────────┘
                   │ 子进程
                   ▼
┌─────────────────────────────────────────────┐
│          FastAPI 后端 (main.py)              │
│  轨道计算 + CZML 格式化                       │
│  监听 127.0.0.1:8000                       │
└──────────────────┬──────────────────────────┘
                   │ 静态文件
                   ▼
┌─────────────────────────────────────────────┐
│          Cesium JS 前端                      │
│  (static/) 三维地球 + 时间动态轨道             │
└─────────────────────────────────────────────┘
```

### 关键设计决策

1. **GUI 作为子进程启动服务器**：GUI 不通过 HTTP 调用 API，而是直接以子进程运行 `uvicorn main:app`，通过 stdout/stderr 解析检测服务器就绪状态。

2. **CZML 格式**：所有轨道数据格式化为 CZML（Cesium Language），而非原始 JSON，因为 Cesium JS 原生支持 CZML 的时间动态场景。

3. **使用 `sgp4` 库**：SGP4 传播算法使用成熟的 `sgp4` 库实现，而非自行编写。

4. **threading.Thread 而非 QThread**：`ProcessManager` 使用 `threading.Thread` 读取子进程输出，因为在 Windows 上 `QThread` 与 pytest 存在兼容性问题。
