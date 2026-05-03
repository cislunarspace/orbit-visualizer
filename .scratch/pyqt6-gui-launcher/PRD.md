---
Status: needs-triage
---

# PyQt6 GUI Launcher for Orbit Visualizer

## Problem Statement

The orbit visualizer is currently launched and configured via command-line arguments and environment variables. There is no interactive control panel for:
- Selecting which orbit types to visualize (state vector, TLE, broadcast ephemeris, precise ephemeris)
- Configuring shared orbit parameters (duration, time step, start time, orbital radius)
- Entering TLE data for a satellite
- Starting and stopping the FastAPI server
- Opening the Cesium visualization in a browser

Users must edit `main.py` or reconstruct URL query strings manually to change orbit configurations.

## Solution

A PyQt6 desktop GUI that acts as a control panel and launcher for the existing FastAPI/Cesium stack. The GUI does not replace the web visualization — it manages the FastAPI server lifecycle and configures orbit parameters before opening Cesium in the browser.

## User Stories

1. As a user, I want to launch the orbit visualizer with a single GUI button, so that I don't need to use the command line.
2. As a user, I want to select which orbit types to visualize via checkboxes (state vector, TLE, broadcast ephemeris, precise ephemeris), so that I can focus on specific satellite data.
3. As a user, I want to configure shared orbit parameters (projection duration in hours, time step in seconds, start time as date+time, orbital radius in meters), so that I can generate orbits for specific time windows and orbital regimes.
4. As a user, I want to pick a TLE satellite from a preset list (ISS, Hubble, Starlink), so that I can quickly visualize well-known satellites without memorizing TLE data.
5. As a user, I want to paste custom TLE line1 and line2 text, so that I can visualize any satellite with a known TLE.
6. As a user, I want to configure the server host and port, with sensible defaults, so that I can avoid port conflicts.
7. As a user, I want to see the server status (stopped / starting / running / failed) in the GUI, so that I know whether the visualization is ready.
8. As a user, I want a clickable browser link in the GUI when the server is running, so that I can open Cesium immediately.
9. As a user, I want an error dialog when the server fails to start (e.g., port already in use), so that I understand what went wrong.
10. As a user, I want to stop the server from the GUI, so that I can cleanly shut down without killing a process manually.
11. As a developer, I want TLE presets and server defaults to be configurable, so that the GUI serves as a usable out-of-the-box tool.

## Implementation Decisions

### Modules to Build

**New: `gui/` — PyQt6 GUI application**

| Module | Responsibility |
|--------|----------------|
| `gui/main_window.py` | Main window; composes all config widgets; manages server process lifecycle |
| `gui/orbit_config.py` | Orbit type checkboxes + global orbit params (hours, step, base_time, r0) |
| `gui/tle_input.py` | TLE preset dropdown + free-text line1/line2 fields |
| `gui/server_config.py` | Host + port input fields with validation |
| `gui/status_bar.py` | Status label (stopped/starting/running/failed) + browser hyperlink |
| `gui/process_manager.py` | Wraps `subprocess.Popen` / `QProcess` for the FastAPI server; exposes start/stop/signals |

**Modified: `main.py`**

- `/api/all` extended to accept `?types=state_vector,tle,broadcast,precise` query parameter
- Only the requested orbit types are generated and returned in the CZML document
- All four types returned by default (backwards-compatible)

**Modified: `run.bat`**

- Instead of launching uvicorn directly, launches the PyQt6 GUI application

### API Contract Change

`GET /api/all?types=state_vector,tle`

- `types`: comma-separated subset of `state_vector`, `tle`, `broadcast`, `precise`
- Returns CZML document containing only the requested orbit types (plus the `document` CZML packet)
- If `types` is absent or empty, all four orbit types are returned (backwards-compatible)

### TLE Presets

| Satellite | TLE Line 1 | TLE Line 2 |
|-----------|-----------|-----------|
| ISS | (current ISS TLE) | (current ISS TLE) |
| Hubble | (representative Hubble TLE) | (representative Hubble TLE) |
| Starlink-1452 | (representative Starlink TLE) | (representative Starlink TLE) |

Default preset: ISS.

### Default Values

| Parameter | Default |
|-----------|---------|
| Server host | `127.0.0.1` |
| Server port | `8000` |
| Projection hours | `24` |
| Time step (seconds) | `60` |
| Base time | current UTC now |
| Orbital radius r0 (m) | `7000000` |
| Orbit types enabled | all four checked |

### Layout

Single scrollable window, sections from top to bottom:
1. **Orbit Types** — 4 checkboxes
2. **Orbit Parameters** — hours, step, base_time (date+time picker), r0
3. **TLE Input** — preset dropdown + line1 + line2 fields
4. **Server Config** — host + port
5. **Control** — Start / Stop button
6. **Status Bar** — status text + browser link (shown when running)

## Testing Decisions

### What makes a good test

- Tests verify **observable external behavior**: server startup/shutdown, API response shape, TLE preset population, GUI signal emission. No testing of internal Qt widget state.
- Tests run the FastAPI app in-process (TestClient) for API-level assertions.

### Modules to test

| Module | Test approach |
|--------|--------------|
| `main.py` — `GET /api/all?types=` | Unit: call endpoint with different `types` values; assert only requested orbit types appear in CZML output |
| `gui/process_manager.py` | Unit: mock subprocess; verify start/stop calls with correct args |
| `gui/tle_input.py` | Unit: verify preset selection populates line1/line2 fields correctly |
| `gui/orbit_config.py` | Unit: verify params are collected into a dict with correct keys and types |

### Prior art

- FastAPI `TestClient` for API endpoint testing
- `pytest-qt` for GUI signal/widget testing if needed

## Out of Scope

- Embedding Cesium or any 3D visualization inside the Qt application (browser remains the visualization surface)
- Saving/loading named configuration profiles
- Authentication or user accounts
- Non-TLE orbit customization per-orbit (all share global params)
- TLS / HTTPS server configuration
- macOS/Linux packaging

## Further Notes

The GUI is a control plane only. The Cesium visualization continues to live in the browser at `http://{host}:{port}/`. The `/api/all` filter change on the backend is a minimal interface adjustment to support per-orbit toggling without changing the existing orbit computation functions.
