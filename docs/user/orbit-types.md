# Orbit Types | 轨道类型说明

**English** | [中文](#中文轨道类型说明)

The system generates four distinct types of satellite orbit visualizations. Each uses a different computational model and serves a different purpose.

---

## 1. State Vector Orbit | 状态向量轨道

**Type ID**: `state_vector`
**Cesium Color**: Cyan `(0, 255, 255, 180)`
**Physical Model**: Simplified circular Keplerian orbit

### How It Works

A circular orbit is computed using a fixed orbital radius and the mean motion equation:

```
ω = sqrt(μ / r³)
θ(t) = ω · t
x = r · cos(θ)
y = r · sin(θ)
z = 0
```

Where `μ = 3.986004418 × 10¹⁴ m³/s²` (Earth's gravitational parameter).

This is a **simplified** model — no perturbation terms (J2, drag, third-body), no eccentricity, no inclination. It is useful for:

- Quick visual demos and UI testing
- Teaching orbital mechanics concepts
- Baseline reference for comparing other orbit types

### Parameters

| Parameter | Field | Default | Effect |
|-----------|-------|---------|--------|
| Orbital radius `r₀` | 轨道半径 | 7,000,000 m | Changes orbit altitude (7,000 km ≈ LEO) |
| Projection hours | 投影时长 | 24 h | Total duration |
| Time step | 时间步长 | 60 s | Point density along the path |

---

## 2. TLE Orbit | TLE 轨道

**Type ID**: `tle`
**Cesium Color**: Yellow `(255, 255, 0, 180)`
**Physical Model**: SGP4/SDP4 propagation

### How It Works

The TLE (Two-Line Element) set is a standardized format encoding the satellite's orbital elements (epoch, inclination, RAAN, eccentricity, argument of perigee, mean anomaly, mean motion). The SGP4 (Simplified General Perturbations, model 4) algorithm propagates these elements forward in time to compute position at any given epoch.

This is the **most accurate** model for real tracked satellites because:
- TLE elements are produced by fitting actual observational data
- SGP4 models include key perturbations (Earth oblateness J2, resonances, etc.)

> **TLE Age**: TLE data represents a snapshot in time. As time passes, prediction error grows. For ISS and most LEO satellites, predictions are accurate to ~1–2 km for about 7 days, degrading significantly after 2–3 weeks.

### Parameters

| Parameter | Field | Default | Effect |
|-----------|-------|---------|--------|
| TLE Line 1 | TLE Line 1 | Preset ISS | First line of TLE element set |
| TLE Line 2 | TLE Line 2 | Preset ISS | Second line of TLE element set |
| Projection hours | 投影时长 | 24 h | Total prediction duration |
| Time step | 时间步长 | 60 s | Point density |

### TLE Format Reference

```
Line 1: NNNNNC NNNNNAAA NNNNN.NNNNNNNN +.NNNNNNNN +NNNNN-N +NNNNN-N N NNNN
Line 2: NNNNN NNN.NNNN NNN.NNNN NNNNNNN NNN.NNNN NNN.NNNN NN.NNNNNNNNNNNNNN
```

| Column | Description | Example (ISS) |
|--------|-------------|---------------|
| 03–07 | NORAD catalog number | 25544 |
| 08 | Classification (U=unclassified) | U |
| 10–11 | International designator year | 98 |
| 12–14 | International designator launch number | 067 |
| 15–17 | Piece of launch | A |
| 19–20 | TLE epoch year | 25 |
| 21–32 | TLE epoch (day of year + fraction) | 123.56789017 |
| 34–43 | First derivative of mean motion | .00000012 |
| 45–52 | Second derivative of mean motion | 00000-0 |
| 54–61 | BSTAR drag term | 12345-6 |
| 63 | Ephemeris type | 0 |
| 65–68 | TLE element set number | 1234 |
| — | Inclination (degrees) | 51.6400 |
| — | Right Ascension of Ascending Node (degrees) | 10.0000 |
| — | Eccentricity (decimal point assumed) | 0.0001234 |
| — | Argument of Perigee (degrees) | 10.0000 |
| — | Mean Anomaly (degrees) | 350.0000 |
| — | Mean Motion (revolutions/day) | 15.48999999 |

---

## 3. Broadcast Ephemeris | 广播星历

**Type ID**: `broadcast`
**Cesium Color**: Green `(0, 255, 0, 180)`
**Physical Model**: Circular orbit at GPS semi-major axis

### How It Works

Simulates the ephemeris broadcast by GPS navigation satellites. The orbit is a circular orbit at the GPS semi-major axis (~26,560 km), representing a typical MEO (Medium Earth Orbit) navigation constellation orbit.

```
a = 26,560,000 m (GPS semi-major axis)
θ(t) = 2π · t / T
x = a · cos(θ)
y = a · sin(θ)
z = 0
```

This is a **simplified** model used for:
- Visualizing the scale difference between LEO and MEO orbits
- Demonstrating navigation satellite coverage concepts
- Testing the broadcast ephemeris API format

### Parameters

| Parameter | Field | Default | Effect |
|-----------|-------|---------|--------|
| Projection hours | 投影时长 | 24 h | Total duration |
| Time step | 时间步长 | 60 s | Point density |

---

## 4. Precise Ephemeris | 精密星历

**Type ID**: `precise`
**Cesium Color**: Red `(255, 0, 0, 180)`
**Physical Model**: Elliptical orbit at precise semi-major axis with inclination offset

### How It Works

Simulates SP3-format scientific precise ephemeris data, typically used for GPS science missions and crustal deformation studies. The orbit uses a higher semi-major axis than GPS (~30,000,000 m) with a small Z-offset to simulate inclination effects.

```
a = 30,000,000 m
z = 100,000 m (inclination effect offset)
```

This is a **simplified** model for:
- Visualizing high-altitude orbits (GEO-adjacent)
- Demonstrating precise ephemeris format structure
- Testing SP3-like data ingestion

### Parameters

| Parameter | Field | Default | Effect |
|-----------|-------|---------|--------|
| Projection hours | 投影时长 | 24 h | Total duration |
| Time step | 时间步长 | 60 s | Point density |

---

## Comparison Table

| Property | State Vector | TLE | Broadcast | Precise |
|----------|-------------|-----|----------|---------|
| Physical model | Simplified Keplerian | SGP4 | Circular MEO | Elliptical |
| Real satellite? | No | Yes | No | No |
| Accuracy | Low | High (TLE-dependent) | Low | Low |
| Data format | Computed | TLE | Computed | Computed |
| Use case | Demo / teaching | Real prediction | Navigation demo | Science demo |
| Altitude | Configurable (r₀) | TLE-dependent | ~20,200 km (GPS) | ~26,700 km |

---

## CZML Output Format

All four orbit types generate data in [CZML (Cesium Language)](https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CZML-Content) format — a JSON schema for time-dynamic 3D visualization.

Each orbit returns a CZML document with two packets:

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
    "path": { "material": { "solidColor": { "color": { "rgba": [0, 255, 255, 180] } } }, "width": 2 },
    "point": { "pixelSize": 8, "color": { "rgba": [0, 255, 255, 180] } }
  }
]
```

- `position.epoch`: ISO 8601 time of the first position point
- `position.cartesian`: Flattened `[x0, y0, z0, x1, y1, z1, ...]` in meters
- `path`: The orbit polyline rendered in Cesium
- `point`: The satellite point marker

---

## 中文轨道类型说明

系统生成四种不同类型的卫星轨道可视化，每种使用不同的计算模型。

### 1. 状态向量轨道

**类型 ID**: `state_vector`
**Cesium 颜色**: 青色 `(0, 255, 255, 180)`
**物理模型**: 简化圆轨道（开普勒）

使用固定轨道半径和匀速圆轨道运动方程计算。适合快速演示、教学和 UI 测试。

### 2. TLE 轨道

**类型 ID**: `tle`
**Cesium 颜色**: 黄色 `(255, 255, 0, 180)`
**物理模型**: SGP4 传播算法

基于 TLE（两行根数）数据，使用 SGP4（简化一般扰动模型第4版）进行轨道预报。是对真实卫星最准确的模型。

> **TLE 时效性**：TLE 数据代表某一时刻的轨道根数。随着时间推移，预报误差会增大。对于 ISS 等 LEO 卫星，TLE 在 7 天内精度约 1–2 km，2–3 周后精度显著下降。

### 3. 广播星历

**类型 ID**: `broadcast`
**Cesium 颜色**: 绿色 `(0, 255, 0, 180)`
**物理模型**: GPS 半长轴处的圆轨道

模拟 GPS 导航卫星广播星历，轨道位于 MEO 中地球轨道高度（约 20,200 km）。

### 4. 精密星历

**类型 ID**: `precise`
**Cesium 颜色**: 红色 `(255, 0, 0, 180)`
**物理模型**: 高轨椭圆轨道

模拟 SP3 格式的科学级精密星历，用于可视化高精度星历数据结构。
