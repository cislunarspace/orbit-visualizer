from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.orbit import LEO_ORBITAL_RADIUS_M
from src.orbit.adapters import (
    broadcast_ephemeris_orbit,
    precise_ephemeris_orbit,
    state_vector_orbit,
    tle_satellite_orbit,
)
from src.orbit.czml import orbit_paths_to_czml, single_orbit_to_czml
from src.orbit.models import OrbitPoint
from src.orbit.request import OrbitRequest
from src.satellites import Satellite, get_default_satellite

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


STATE_VECTOR_ID = "状态向量"
BROADCAST_ID = "广播星历"
PRECISE_ID = "精密星历"


def _utc_str(dt: datetime) -> str:
    """Format a timezone-aware UTC datetime as ISO 8601 with Z suffix."""
    return dt.isoformat().replace("+00:00", "Z")


def generate_state_vector_orbit(
    hours: int = 24,
    step: int = 60,
    base_time: datetime | None = None,
    radius_m: float = LEO_ORBITAL_RADIUS_M,
) -> list[OrbitPoint]:
    """Generate the state-vector orbit through the shared OrbitPoint adapter."""
    return state_vector_orbit(hours=hours, step=step, base_time=base_time, radius_m=radius_m)


def tle_to_orbit(
    tle_line1: str,
    tle_line2: str,
    hours: int = 24,
    step: int = 60,
    base_time: datetime | None = None,
) -> list[OrbitPoint]:
    """Generate a TLE orbit through the shared Satellite adapter."""
    satellite = Satellite(name="Custom", tle_line1=tle_line1, tle_line2=tle_line2)
    return tle_satellite_orbit(satellite, hours=hours, step=step, base_time=base_time)


def generate_broadcast_ephemeris(hours: int = 24, step: int = 60, base_time: datetime | None = None) -> list[OrbitPoint]:
    """Generate a broadcast ephemeris orbit through the shared adapter."""
    return broadcast_ephemeris_orbit(hours=hours, step=step, base_time=base_time)


def generate_precise_ephemeris(hours: int = 24, step: int = 60, base_time: datetime | None = None) -> list[OrbitPoint]:
    """Generate a precise ephemeris orbit through the shared adapter."""
    return precise_ephemeris_orbit(hours=hours, step=step, base_time=base_time)


def make_czml(name: str, data: list[OrbitPoint], color: list[int]) -> list[dict]:
    """Format one OrbitPoint path as a CZML document."""
    return single_orbit_to_czml(name, data, color)


@app.get("/")
def index() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/api/orbit/state_vector")
def orbit_state_vector() -> list[dict]:
    data = generate_state_vector_orbit()
    return make_czml(f"{STATE_VECTOR_ID}(仿真)", data, [0, 255, 255, 180])


@app.get("/api/orbit/tle")
def orbit_tle() -> list[dict]:
    sat = get_default_satellite()
    data = tle_satellite_orbit(sat)
    return make_czml("TLE(低轨预报)", data, [255, 255, 0, 180])


@app.get("/api/orbit/broadcast")
def orbit_broadcast() -> list[dict]:
    data = generate_broadcast_ephemeris()
    return make_czml(f"{BROADCAST_ID}(导航)", data, [0, 255, 0, 180])


@app.get("/api/orbit/precise")
def orbit_precise() -> list[dict]:
    data = generate_precise_ephemeris()
    return make_czml(f"{PRECISE_ID}(科学)", data, [255, 0, 0, 180])


@app.get("/api/all")
def all_orbits(types: str | None = None) -> list[dict]:
    t0 = datetime.now(timezone.utc)
    request = OrbitRequest.from_query(types=types, base_time=t0, ignore_unknown=True)
    paths = []

    if "state_vector" in request.types:
        paths.append(
            (
                STATE_VECTOR_ID,
                state_vector_orbit(
                    hours=request.hours,
                    step=request.step,
                    base_time=t0,
                    radius_m=request.radius_m or LEO_ORBITAL_RADIUS_M,
                ),
                [0, 255, 255, 180],
            )
        )

    if "tle" in request.types:
        paths.append(
            (
                "TLE",
                tle_satellite_orbit(request.satellite, hours=request.hours, step=request.step, base_time=t0),
                [255, 255, 0, 180],
            )
        )

    if "broadcast" in request.types:
        paths.append(
            (
                BROADCAST_ID,
                broadcast_ephemeris_orbit(hours=request.hours, step=request.step, base_time=t0),
                [0, 255, 0, 180],
            )
        )

    if "precise" in request.types:
        paths.append(
            (
                PRECISE_ID,
                precise_ephemeris_orbit(hours=request.hours, step=request.step, base_time=t0),
                [255, 0, 0, 180],
            )
        )

    return orbit_paths_to_czml(paths)
