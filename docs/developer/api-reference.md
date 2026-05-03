# API Reference | API 参考

**English** | [中文](#中文-api-参考)

Base URL: `http://127.0.0.1:8000`

---

## Endpoints

### `GET /`

Serves the Cesium JavaScript viewer.

**Response**: `text/html`

Returns the contents of `static/index.html`.

---

### `GET /api/all`

Returns all requested orbit types as a CZML document. Supports filtering via the `types` query parameter.

**Query Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `types` | `string` | (all types) | Comma-separated list of orbit type IDs |

**Orbit Type IDs**

| ID | Orbit Type |
|----|------------|
| `state_vector` | State vector orbit |
| `tle` | TLE orbit |
| `broadcast` | Broadcast ephemeris |
| `precise` | Precise ephemeris |

**Examples**

```
GET /api/all                         # All 4 orbit types
GET /api/all?types=state_vector      # Only state vector
GET /api/all?types=state_vector,tle  # State vector + TLE
GET /api/all?types=tle,broadcast     # TLE + broadcast
```

**Response**: `application/json`

```json
[
  {
    "id": "document",
    "version": "1.0",
    "clock": {
      "interval": "2025-05-03T00:00:00Z/2025-05-04T00:00:00Z",
      "currentTime": "2025-05-03T00:00:00Z",
      "multiplier": 60
    }
  },
  {
    "id": "轨道名称",
    "name": "轨道名称",
    "position": {
      "epoch": "2025-05-03T00:00:00Z",
      "cartesian": [x0, y0, z0, x1, y1, z1, ...]
    },
    "path": {
      "material": { "solidColor": { "color": { "rgba": [R, G, B, A] } } },
      "width": 2,
      "show": true
    },
    "point": {
      "pixelSize": 8,
      "color": { "rgba": [R, G, B, A] }
    }
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | `"document"` or orbit type name |
| `position.epoch` | ISO 8601 string | Time of first position point |
| `position.cartesian` | float[] | Flattened [x, y, z, x, y, z, ...] in meters |
| `path.material.solidColor.color.rgba` | int[4] | RGBA color (0–255) |
| `point.pixelSize` | int | Satellite point size in pixels |
| `clock.interval` | ISO 8601 interval | Start/end of orbit time range |
| `clock.currentTime` | ISO 8601 string | Initial playback time |
| `clock.multiplier` | int | Playback speed multiplier |

---

### `GET /api/orbit/state_vector`

Returns a CZML document containing only the state vector orbit.

**Response**: Same as `GET /api/all`, with one orbit packet.

**Color**: Cyan `(0, 255, 255, 180)`

---

### `GET /api/orbit/tle`

Returns a CZML document containing only the TLE orbit, using the default ISS TLE.

**Response**: Same as `GET /api/all`, with one orbit packet.

**Color**: Yellow `(255, 255, 0, 180)`

---

### `GET /api/orbit/broadcast`

Returns a CZML document containing only the broadcast ephemeris orbit.

**Response**: Same as `GET /api/all`, with one orbit packet.

**Color**: Green `(0, 255, 0, 180)`

---

### `GET /api/orbit/precise`

Returns a CZML document containing only the precise ephemeris orbit.

**Response**: Same as `GET /api/all`, with one orbit packet.

**Color**: Red `(255, 0, 0, 180)`

---

## Static Files

### `GET /static/{path}`

Serves static assets from the `static/` directory. Used by the frontend to load Cesium JS and related assets.

---

## Error Responses

| Status | Cause |
|--------|-------|
| `404 Not Found` | Invalid path |
| `422 Unprocessable Entity` | Invalid query parameter value |

No authentication required. CORS is enabled for all origins in development mode.

---

## Python Client Example

```python
import requests

# Fetch all orbit types
response = requests.get("http://127.0.0.1:8000/api/all")
czml_doc = response.json()

# Fetch only TLE orbit
response = requests.get("http://127.0.0.1:8000/api/all?types=tle")
czml_doc = response.json()

# Fetch multiple types
response = requests.get("http://127.0.0.1:8000/api/all?types=state_vector,tle,broadcast")
czml_doc = response.json()
```

---

## CZML Packet Structure

Each non-document packet has this structure:

```python
{
    "id": "轨道名称",          # Unique identifier for this orbit
    "name": "轨道名称",        # Display name in Cesium UI
    "position": {
        "epoch": "2025-05-03T00:00:00Z",  # Start time of orbit
        "cartesian": [
            x0, y0, z0,     # First position (meters)
            x1, y1, z1,     # Second position
            ...
        ]
    },
    "path": {
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [R, G, B, A]  # 0-255 per channel
                }
            }
        },
        "width": 2,
        "show": True
    },
    "point": {
        "pixelSize": 8,
        "color": {
            "rgba": [R, G, B, A]
        }
    }
}
```

The `cartesian` array uses the [Cesium WGS84 Earth-fixed frame](https://cesium.com/learn/cesiumjs/ref-doc/Cartesian3.html) (ECEF), with coordinates in meters from the Earth's center of mass.

---

## 中文 API 参考

基础 URL：`http://127.0.0.1:8000`

### `GET /`

返回 Cesium 可视化页面（`static/index.html`）。

### `GET /api/all`

返回请求的轨道类型，格式为 CZML 文档。支持通过 `types` 查询参数过滤。

**查询参数**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `types` | string | 全部类型 | 逗号分隔的轨道类型 ID 列表 |

**轨道类型 ID**

| ID | 轨道类型 |
|----|----------|
| `state_vector` | 状态向量轨道 |
| `tle` | TLE 轨道 |
| `broadcast` | 广播星历 |
| `precise` | 精密星历 |

**示例**

```
GET /api/all                          # 返回全部 4 种轨道
GET /api/all?types=state_vector      # 仅状态向量
GET /api/all?types=state_vector,tle  # 状态向量 + TLE
```

**响应格式**

返回 CZML JSON 文档。第一个 packet 是 `document`（时钟配置），后续 packet 是各轨道数据。

```json
[
  {
    "id": "document",
    "version": "1.0",
    "clock": { ... }
  },
  {
    "id": "轨道名称",
    "name": "轨道名称",
    "position": {
      "epoch": "2025-05-03T00:00:00Z",
      "cartesian": [x0, y0, z0, x1, y1, z1, ...]
    },
    "path": { ... },
    "point": { ... }
  }
]
```

### `GET /api/orbit/{type}`

单独获取某种轨道类型：
- `GET /api/orbit/state_vector` — 状态向量（青色）
- `GET /api/orbit/tle` — TLE（黄色）
- `GET /api/orbit/broadcast` — 广播星历（绿色）
- `GET /api/orbit/precise` — 精密星历（红色）

### 错误响应

| 状态码 | 原因 |
|--------|------|
| `404 Not Found` | 路径不存在 |
| `422 Unprocessable Entity` | 查询参数值无效 |

### Python 调用示例

```python
import requests

# 获取所有轨道
r = requests.get("http://127.0.0.1:8000/api/all")
czml = r.json()

# 只获取 TLE
r = requests.get("http://127.0.0.1:8000/api/all?types=tle")
czml = r.json()
```
