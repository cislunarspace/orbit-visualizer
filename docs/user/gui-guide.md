# GUI User Guide | GUI 使用指南

**English** | [中文](#中文-gui-使用指南)

Launch the GUI with:

```bash
uv run python -m gui
```

The GUI provides a single window with all controls organized into collapsible sections.

---

## Interface Overview

### Window Layout

```
┌─────────────────────────────────────────┐
│  卫星轨道可视化器                         │
│                                         │
│  ▼ 轨道类型 (checkboxes)                │
│  ▼ 轨道参数 (hours, step, time, r0)     │
│  ▼ TLE 输入 (preset + line1/2)          │
│  ▼ 服务器配置 (host, port)               │
│                                         │
│  [ 启动服务器 ]                          │
│                                         │
│  状态: 已停止              [打开浏览器 →]  │
└─────────────────────────────────────────┘
```

---

## Section: 轨道类型 (Orbit Types)

Four checkboxes, all checked by default. Each corresponds to one orbit visualization layer in Cesium.

| Checkbox | Orbit Type | Color in Cesium |
|----------|------------|-----------------|
| 状态向量 (state_vector) | Simulated state vector orbit | Cyan |
| TLE (tle) | SGP4 satellite prediction | Yellow |
| 广播星历 (broadcast) | Simulated GPS navigation orbit | Green |
| 精密星历 (precise) | Simulated precise science orbit | Red |

Uncheck any type to exclude it from visualization. The server will not generate data for unchecked types.

---

## Section: 轨道参数 (Orbit Parameters)

Controls the time range and resolution of the generated orbits.

| Field | Chinese Label | Default | Range | Description |
|-------|--------------|---------|-------|-------------|
| Hours | 投影时长 | 24 hours | 1–168 | Total time span to project |
| Step | 时间步长 | 60 seconds | 1–3600 | Time step between orbit points |
| Base Time | 起始时间 | now (UTC) | — | Starting time for the orbit projection |
| Radius | 轨道半径 | 7,000,000 m | 6e6–10e7 | Reference orbital radius (for state vector orbit) |

### Practical Tips

- **Short arcs** (1–6 hours, step 30–60s): Good for quick previews
- **Long arcs** (24–72 hours, step 60–300s): Better for understanding orbital decay or ground track patterns
- **Base Time**: Changing this shifts the entire orbit forward or backward in time. Useful for predicting future passes.

---

## Section: TLE 输入 (TLE Input)

TLE (Two-Line Element) set input for real satellite orbit propagation.

| Control | Description |
|---------|-------------|
| Satellite dropdown | Select preset: ISS, Hubble, Starlink-1452, or Custom |
| TLE Line 1 | First line of the TLE element set |
| TLE Line 2 | Second line of the TLE element set |

### Presets

| Satellite | NORAD ID | Notes |
|----------|----------|-------|
| ISS | 25544 | International Space Station |
| Hubble | 20580 | Hubble Space Telescope |
| Starlink-1452 | 44083 | SpaceX Starlink batch 1452 |

To use a different satellite, select **Custom** and enter the TLE lines manually. TLE data for any satellite can be obtained from [Space-Track.org](https://www.space-track.org) or [Celestrak](https://celestrak.org).

> **Note**: TLE data degrades over time. For accurate propagation, use a recent TLE (less than 30 days old is ideal).

---

## Section: 服务器配置 (Server Configuration)

| Control | Default | Description |
|---------|---------|-------------|
| Host | `127.0.0.1` | Interface to bind to |
| Port | `8000` | TCP port number (1024–65535) |

### Port Conflicts

If port `8000` is already in use, change the port here and click **启动服务器**. The browser link in the status bar will update to the new port.

---

## Start / Stop Button

| State | Button Label | Behavior |
|-------|-------------|----------|
| Server stopped | 启动服务器 | Starts the FastAPI server |
| Server starting | (disabled) | Waiting for server to become ready |
| Server running | 停止服务器 | Stops the server |

When the server is ready, the status bar shows **状态: 运行中** and a **打开浏览器 →** link appears. Clicking it opens [http://127.0.0.1:8000](http://127.0.0.1:8000) in your default browser.

---

## Status Bar

Located at the bottom of the window. Shows the current server state.

| Status | Label | Browser Link |
|--------|-------|-------------|
| Stopped | 状态: 已停止 | Hidden |
| Starting | 状态: 启动中... | Hidden |
| Running | 状态: 运行中 | Visible: "打开浏览器 →" |
| Failed | 状态: 启动失败 | Hidden |

---

## Built-in Help

Click **帮助** (Help) in the title bar menu (or press `F1`) to open the built-in help dialog with the full user manual.

---

## 中文 GUI 使用指南

启动 GUI：

```bash
uv run python -m gui
```

界面布局如图所示，所有控件按功能分组。

### 界面布局

```
┌─────────────────────────────────────────┐
│  卫星轨道可视化器                         │
│                                         │
│  ▼ 轨道类型 (复选框)                       │
│  ▼ 轨道参数 (时长、步长、时间、半径)         │
│  ▼ TLE 输入 (预设 + 行1/行2)              │
│  ▼ 服务器配置 (主机、端口)                  │
│                                         │
│  [ 启动服务器 ]                            │
│                                         │
│  状态: 已停止              [打开浏览器 →]   │
└─────────────────────────────────────────┘
```

### 轨道类型

四个复选框，默认全部选中。取消选中则不在 Cesium 中渲染对应轨道。

| 复选框 | 轨道类型 | Cesium 颜色 |
|--------|----------|-------------|
| 状态向量 (state_vector) | 仿真状态向量轨道 | 青色 |
| TLE (tle) | SGP4 卫星预报 | 黄色 |
| 广播星历 (broadcast) | 模拟 GPS 导航卫星 | 绿色 |
| 精密星历 (precise) | 模拟精密科学轨道 | 红色 |

### 轨道参数

| 字段 | 默认值 | 说明 |
|------|--------|------|
| 投影时长 | 24 小时 | 轨道投影的总时间跨度 |
| 时间步长 | 60 秒 | 相邻轨道点之间的时间间隔 |
| 起始时间 | 当前 UTC 时间 | 轨道投影的起始时刻 |
| 轨道半径 | 7,000,000 m | 状态向量轨道的参考轨道半径 |

### TLE 输入

支持三种预设卫星（ISS、Hubble、Starlink-1452），或选择"Custom"手动输入任意卫星的 TLE 数据。

> **提示**：TLE 数据会随时间衰减。如需精确预报，请使用 30 天以内的 TLE 数据。可从 [Space-Track.org](https://www.space-track.org) 或 [Celestrak](https://celestrak.org) 获取。

### 服务器配置

默认主机 `127.0.0.1`，端口 `8000`。若端口被占用，更改端口后点击"启动服务器"。

### 状态栏

底部显示服务器当前状态。服务器就绪后，点击"打开浏览器 →"可在浏览器中打开可视化页面。

### 内置帮助

按 `F1` 或通过菜单打开内置帮助对话框，查看完整用户手册。
