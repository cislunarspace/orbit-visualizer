# Quick Start Guide | 快速开始指南

**English** | [中文](#中文快速开始)

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended package manager)

## Installation

```bash
# Clone the repository
git clone https://github.com/cislunarspace/orbit-visualizer.git
cd orbit-visualizer

# Install dependencies with uv
uv sync
```

## Running the Application | 运行应用

### Option 1: GUI Control Panel (Recommended)

Launch the PyQt6 desktop application with the full control panel:

```bash
uv run python -m gui
```

The GUI will:
1. Start the FastAPI server internally on `127.0.0.1:8000`
2. Automatically open your default browser to the visualization page
3. Show server status in the status bar at the bottom

To stop the server, click **停止服务器** (Stop Server) or close the window.

### Option 2: Direct Server

Run the FastAPI server directly without the GUI:

```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) manually.

## Project Structure

```
orbit-visualizer/
├── main.py              # FastAPI server + orbit generation logic
├── gui/                 # PyQt6 GUI package
│   ├── main_window.py   # Main application window
│   ├── orbit_config.py  # Orbit type + param widgets
│   ├── tle_input.py     # TLE preset selector
│   ├── server_config.py # Host/port configuration
│   ├── status_bar.py    # Server status display
│   └── process_manager.py # Server subprocess manager
├── src/                 # Core computation package
│   ├── orbit/           # Orbital mechanics (Keplerian constants)
│   └── satellites/      # TLE satellite data
├── static/              # Frontend assets (Cesium JS, HTML)
└── tests/               # Test suite (31 tests)
```

## Running Tests

```bash
uv run pytest
```

All 31 tests should pass.

---

## 中文快速开始

## 环境要求

- Python 3.10+
- 推荐使用 [uv](https://github.com/astral-sh/uv) 包管理器

## 安装

```bash
git clone https://github.com/cislunarspace/orbit-visualizer.git
cd orbit-visualizer
uv sync
```

## 运行应用

### 方式一：GUI 控制面板（推荐）

启动 PyQt6 桌面应用程序：

```bash
uv run python -m gui
```

GUI 将自动：
1. 在后台启动 FastAPI 服务器（`127.0.0.1:8000`）
2. 自动打开浏览器访问可视化页面
3. 在底部状态栏显示服务器状态

关闭窗口或点击 **停止服务器** 即可停止服务器。

### 方式二：直接启动服务器

不启动 GUI，直接运行 API 服务器：

```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

然后手动访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 项目结构

| 目录/文件 | 说明 |
|-----------|------|
| `main.py` | FastAPI 服务器 + 轨道生成逻辑 |
| `gui/` | PyQt6 GUI 包 |
| `src/orbit/` | 轨道力学计算（开普勒常数） |
| `src/satellites/` | TLE 卫星数据 |
| `static/` | 前端资源（Cesium JS、HTML） |
| `tests/` | 测试套件（31 个测试） |

## 运行测试

```bash
uv run pytest
```

所有 31 个测试应全部通过。
