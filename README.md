# Orbit Visualizer | 卫星轨道可视化器

**English** | [中文](#中文)

Multi-source satellite orbit comprehensive visualization system, powered by FastAPI + Cesium.

![Orbit Visualizer](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features | 功能特点

- **4 Orbit Types** — State vector, TLE (SGP4), broadcast ephemeris, precise ephemeris
- **Cesium 3D Visualization** — Interactive time-dynamic globe
- **PyQt6 Desktop GUI** — Local control panel with one-click server launch
- **REST API** — Filter orbits via `?types=` query parameter

## Quick Start | 快速开始

### Installation | 安装

```bash
git clone https://github.com/cislunarspace/orbit-visualizer.git
cd orbit-visualizer
uv sync
```

### Run | 运行

```bash
# Launch the GUI control panel (recommended)
uv run python -m gui

# Or run the API server directly
uv run uvicorn main:app --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Documentation | 文档

| Document | Description |
|----------|-------------|
| [Quick Start](docs/quick-start.md) | Installation and first run | 安装与首次运行 |
| [User Guide — GUI](docs/user/gui-guide.md) | GUI interface walkthrough | GUI 界面使用说明 |
| [User Guide — Orbit Types](docs/user/orbit-types.md) | Orbit type explanations | 轨道类型说明 |
| [Developer — Architecture](docs/developer/architecture.md) | System architecture | 系统架构 |
| [Developer — API Reference](docs/developer/api-reference.md) | API endpoint reference | API 接口参考 |
| [Developer — Frontend](docs/developer/frontend.md) | Cesium frontend guide | Cesium 前端说明 |
| [Developer — Development](docs/developer/development.md) | Extending the project | 开发扩展指南 |

Full documentation: [docs/README.md](docs/README.md)

## License | 许可证

MIT License

---

## 中文

卫星轨道综合可视化系统，基于 FastAPI + Cesium 构建，支持 4 种轨道类型和 PyQt6 桌面控制面板。

### 功能特点

- **4 种轨道类型** — 状态向量、TLE（SGP4）、广播星历、精密星历
- **Cesium 三维可视化** — 交互式时间动态地球
- **PyQt6 桌面 GUI** — 一键启动本地服务器的图形控制面板
- **REST API** — 通过 `?types=` 查询参数过滤轨道类型

### 安装与运行

```bash
git clone https://github.com/cislunarspace/orbit-visualizer.git
cd orbit-visualizer
uv sync
uv run python -m gui
```

完整文档请参阅 [docs/README.md](docs/README.md)。
