# Frontend Guide | 前端说明

**English** | [中文](#中文前端说明)

## Overview

The frontend is a single-page application served from `static/index.html`. It uses [Cesium JS](https://cesium.com/platform/cesiumjs/) to render time-dynamic satellite orbits on a 3D globe.

---

## File Structure

```
static/
└── index.html      # Cesium viewer (single HTML file)
```

The Cesium JS library is loaded from CDN. No build step is required.

---

## How It Works

### Initialization Flow

```
index.html loads in browser
    │
    ▼
Cesium Ion is initialized (or basic Cesium with default imagery)
    │
    ▼
GET /api/all?types=state_vector,tle,broadcast,precise
    │
    ▼
CZML data loaded as CZML DataSource
    │
    ▼
Orbits + satellite points rendered on 3D globe
    │
    ▼
Cesium timeline and clock controls are active
```

### Key Cesium Components

| Component | Purpose |
|-----------|---------|
| `Cesium.Viewer` | Main globe widget with imagery, terrain, controls |
| `Cesium.CzmlDataSource` | Processes CZML packets and creates entities |
| `viewer.entities` | Individual orbit paths and satellite points |
| `viewer.scene.clock` | Time control for playback |

### CZML Data Flow

```
main.py: GET /api/all
    │
    ▼
make_czml() builds:
    [
      { "id": "document", "clock": {...} },   ← Clock config
      { "id": "状态向量", "position": {...} },  ← Orbit entity
      ...
    ]
    │
    ▼
Cesium.CzmlDataSource.load(czmlDoc)
    │
    ▼
Entities auto-created from CZML packets:
    - document packet → clock settings
    - orbit packets → polyline (path) + point (satellite marker)
```

---

## Cesium Clock Configuration

The `document` CZML packet configures the Cesium clock:

```json
{
  "id": "document",
  "clock": {
    "interval": "2025-05-03T00:00:00Z/2025-05-04T00:00:00Z",
    "currentTime": "2025-05-03T00:00:00Z",
    "multiplier": 60
  }
}
```

| Field | Value | Meaning |
|-------|-------|---------|
| `interval` | Start/End ISO8601 | Total time range of orbit data |
| `currentTime` | Start ISO8601 | Initial playback time |
| `multiplier` | 60 | Playback speed: 60× real time |

### Changing Playback Speed

The `multiplier` value can be adjusted. Common values:

| Multiplier | Effective Speed |
|------------|----------------|
| 1 | Real-time (1 second = 1 second) |
| 60 | 1 minute of orbit per real second |
| 300 | 5 minutes per second |
| 3600 | 1 hour per second |

To change: edit `main.py` in the `make_czml()` function's clock configuration.

---

## Imagery and Terrain

The default Cesium viewer uses:

- **Imagery**: Cesium's default Bing Maps / Sentinel-2 hybrid (via Cesium Ion default token, or fallback to OpenStreetMap if configured)
- **Terrain**: Cesium's default World Terrain (via Cesium Ion)

To use a different imagery provider, modify `index.html`:

```javascript
const viewer = new Cesium.Viewer('cesiumContainer', {
  imageryProvider: new Cesium.OpenStreetMapImageryProvider({
    url: 'https://tile.openstreetmap.org/'
  }),
  baseLayerPicker: false,
  geocoder: false
});
```

---

## Customization

### Change Default Orbit Colors

Edit the `make_czml()` function in `main.py`:

```python
# State vector: Cyan
make_czml("状态向量", sv_data, [0, 255, 255, 180])

# TLE: Yellow
make_czml("TLE", tle_data, [255, 255, 0, 180])

# Broadcast: Green
make_czml("广播星历", brd_data, [0, 255, 0, 180])

# Precise: Red
make_czml("精密星历", pre_data, [255, 0, 0, 180])
```

Color format: `[R, G, B, A]` with values 0–255.

### Change Path Width

Edit the `path.width` value in `make_czml()`:

```python
"path": {
    "material": {"solidColor": {"color": {"rgba": color}}},
    "width": 3,  # Increase for thicker orbit lines
    "show": True,
},
```

### Change Point Size

```python
"point": {
    "pixelSize": 10,  # Increase for larger satellite markers
    "color": {"rgba": color},
},
```

### Enable Terrain Lighting

Add to `index.html` after viewer creation:

```javascript
viewer.scene.globe.enableLighting = true;
```

---

## HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Orbit Visualizer</title>
  <script src="https://cesium.com/downloads/cesiumjs/releases/1.114/Build/Cesium/Cesium.js"></script>
  <link href="https://cesium.com/downloads/cesiumjs/releases/1.114/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
  <style>
    html, body, #cesiumContainer {
      width: 100%; height: 100%; margin: 0; padding: 0;
    }
  </style>
</head>
<body>
  <div id="cesiumContainer"></div>
  <script>
    // Initialize Cesium viewer
    // Load CZML from API
  </script>
</body>
</html>
```

---

## Troubleshooting

### Orbits not appearing

1. Check browser console for CORS errors or network failures
2. Verify the FastAPI server is running: `http://127.0.0.1:8000/api/all`
3. Check that CZML `position.cartesian` values are finite numbers (non-NaN)

### Cesium blank screen

1. Check if Cesium Ion token is required for your imagery provider
2. Try switching to OpenStreetMap imagery provider (see above)

### Clock not animating

1. In Cesium UI, ensure the timeline (bottom bar) is expanded
2. Click the play button on the timeline to start animation
3. Check `clock.multiplier` in the CZML document packet

---

## 中文前端说明

### 概述

前端是从 `static/index.html` 提供的单页应用，使用 [Cesium JS](https://cesium.com/platform/cesiumjs/) 在三维地球上渲染时间动态卫星轨道。

### 工作流程

```
index.html 加载
    │
    ▼
Cesium JS 初始化
    │
    ▼
GET /api/all?types=...
    │
    ▼
CZML 数据通过 CzmlDataSource 加载
    │
    ▼
轨道线和卫星点渲染到地球上
    │
    ▼
Cesium 时间线控制可播放
```

### 自定义

**修改轨道颜色**：编辑 `main.py` 中的 `make_czml()` 函数中的 RGBA 颜色值。

**修改线宽**：编辑 `main.py` 中 `path.width` 的值。

**修改点大小**：编辑 `main.py` 中 `point.pixelSize` 的值。

**启用地形光照**：在 `index.html` 的 Cesium 初始化代码后添加 `viewer.scene.globe.enableLighting = true;`。

### 常见问题

**轨道不显示**：检查浏览器控制台是否有 CORS 错误或网络错误，确认服务器正在运行。

**Cesium 空白屏幕**：可能需要 Cesium Ion token，可切换到 OpenStreetMap 影像源。

**时钟不播放**：在 Cesium UI 中展开底部时间线，点击播放按钮。
