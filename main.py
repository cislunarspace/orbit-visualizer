from datetime import datetime, timedelta, timezone

import numpy as np
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sgp4.api import Satrec, jday

from src.orbit import (
    EARTH_GRAVITATIONAL_PARAMETER,
    GPS_SEMI_MAJOR_AXIS_M,
    LEO_ORBITAL_RADIUS_M,
    PRECISE_SEMI_MAJOR_AXIS_M,
)
from src.satellites import get_default_satellite


def _utc_str(dt: datetime) -> str:
    """Format a timezone-aware UTC datetime as ISO 8601 with Z suffix."""
    return dt.isoformat().replace("+00:00", "Z")


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# 1. 状态向量（仿真轨道：直接使用 XYZ/VxVyVz）
def generate_state_vector_orbit(hours: int = 24, step: int = 60, base_time: datetime | None = None) -> list[dict]:
    """仿真状态向量轨道：近地卫星（ECI 坐标系）"""
    t0 = base_time or datetime.now(timezone.utc)
    mu = EARTH_GRAVITATIONAL_PARAMETER
    r0 = LEO_ORBITAL_RADIUS_M

    pos_list = []
    for i in range(0, hours * 3600, step):
        theta = np.sqrt(mu / r0**3) * i
        c, s = np.cos(theta), np.sin(theta)
        x, y, z = r0 * c, r0 * s, 0.0
        time = _utc_str(t0 + timedelta(seconds=i))
        pos_list.append({"time": time, "pos": [x, y, z]})
    return pos_list


# 2. TLE 轨道（SGP4 低轨卫星预报）
def tle_to_orbit(tle_line1: str, tle_line2: str, hours: int = 24, step: int = 60, base_time: datetime | None = None) -> list[dict]:
    """由两行根数计算卫星轨道位置（SGP4 模型）"""
    sat = Satrec.twoline2rv(tle_line1, tle_line2)
    t0 = base_time or datetime.now(timezone.utc)
    data = []

    for i in range(0, hours * 3600, step):
        t = t0 + timedelta(seconds=i)
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        _, r, _ = sat.sgp4(jd, fr)
        pos_km = [r[0] * 1000, r[1] * 1000, r[2] * 1000]
        data.append({"time": _utc_str(t), "pos": pos_km})
    return data


# 3. 广播星历（模拟导航卫星轨道）
def generate_broadcast_ephemeris(hours: int = 24, step: int = 60, base_time: datetime | None = None) -> list[dict]:
    """模拟 GPS 导航卫星广播星历（MEO 轨道）"""
    t0 = base_time or datetime.now(timezone.utc)
    a = GPS_SEMI_MAJOR_AXIS_M
    data = []

    for i in range(0, hours * 3600, step):
        theta = 2 * np.pi * i / (hours * 3600)
        x = a * np.cos(theta)
        y = a * np.sin(theta)
        z = 0.0
        t = t0 + timedelta(seconds=i)
        data.append({"time": _utc_str(t), "pos": [x, y, z]})
    return data


# 4. 精密星历（模拟 SP3 科学级高精度轨道）
def generate_precise_ephemeris(hours: int = 24, step: int = 60, base_time: datetime | None = None) -> list[dict]:
    """模拟 SP3 格式科学级精密星历"""
    t0 = base_time or datetime.now(timezone.utc)
    a = PRECISE_SEMI_MAJOR_AXIS_M
    data = []

    for i in range(0, hours * 3600, step):
        theta = 2 * np.pi * i / (hours * 3600) + 0.1
        x = a * np.cos(theta)
        y = a * np.sin(theta)
        z = 100e3  # 轨道倾角等效偏移
        t = t0 + timedelta(seconds=i)
        data.append({"time": _utc_str(t), "pos": [x, y, z]})
    return data


# 5. 生成 CZML（Cesium 标准格式）
def make_czml(name: str, data: list[dict], color: list[int]) -> list[dict]:
    """将轨道数据转换为 CZML 格式（Cesium 三维可视化）"""
    return [
        {
            "id": "document",
            "version": "1.0",
            "clock": {
                "interval": f"{data[0]['time']}/{data[-1]['time']}",
                "currentTime": data[0]["time"],
                "multiplier": 60,
            },
        },
        {
            "id": name,
            "name": name,
            "position": {
                "epoch": data[0]["time"],
                "cartesian": [p for item in data for p in item["pos"]],
            },
            "path": {
                "material": {"solidColor": {"color": {"rgba": color}}},
                "width": 2,
                "show": True,
            },
            "point": {
                "pixelSize": 8,
                "color": {"rgba": color},
            },
        },
    ]


# ---- API 接口 ----


@app.get("/")
def index() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/api/orbit/state_vector")
def orbit_state_vector() -> list[dict]:
    data = generate_state_vector_orbit()
    return make_czml("状态向量(仿真)", data, [0, 255, 255, 180])


@app.get("/api/orbit/tle")
def orbit_tle() -> list[dict]:
    sat = get_default_satellite()
    data = tle_to_orbit(sat.tle_line1, sat.tle_line2)
    return make_czml("TLE(低轨预报)", data, [255, 255, 0, 180])


@app.get("/api/orbit/broadcast")
def orbit_broadcast() -> list[dict]:
    data = generate_broadcast_ephemeris()
    return make_czml("广播星历(导航)", data, [0, 255, 0, 180])


@app.get("/api/orbit/precise")
def orbit_precise() -> list[dict]:
    data = generate_precise_ephemeris()
    return make_czml("精密星历(科学)", data, [255, 0, 0, 180])


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

    return [{"id": "document", "version": "1.0"}, *czml]
