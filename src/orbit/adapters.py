"""Orbit computation adapters that produce OrbitPoint values."""

from datetime import datetime, timedelta, timezone

import numpy as np
from sgp4.api import Satrec, jday

from src.satellites import Satellite

from .constants import (
    EARTH_GRAVITATIONAL_PARAMETER,
    GPS_SEMI_MAJOR_AXIS_M,
    LEO_ORBITAL_RADIUS_M,
    PRECISE_SEMI_MAJOR_AXIS_M,
)
from .models import OrbitPoint


def _base_time(base_time: datetime | None) -> datetime:
    return base_time or datetime.now(timezone.utc)


def state_vector_orbit(
    hours: int = 24,
    step: int = 60,
    base_time: datetime | None = None,
    radius_m: float = LEO_ORBITAL_RADIUS_M,
) -> list[OrbitPoint]:
    """Generate a simulated circular LEO state-vector orbit."""
    t0 = _base_time(base_time)
    points: list[OrbitPoint] = []
    for i in range(0, hours * 3600, step):
        theta = np.sqrt(EARTH_GRAVITATIONAL_PARAMETER / radius_m**3) * i
        c, s = np.cos(theta), np.sin(theta)
        points.append(OrbitPoint(time=t0 + timedelta(seconds=i), position_m=(radius_m * c, radius_m * s, 0.0)))
    return points


def tle_satellite_orbit(
    satellite: Satellite,
    hours: int = 24,
    step: int = 60,
    base_time: datetime | None = None,
) -> list[OrbitPoint]:
    """Propagate a Satellite TLE through SGP4."""
    satrec = Satrec.twoline2rv(satellite.tle_line1, satellite.tle_line2)
    t0 = _base_time(base_time)
    points: list[OrbitPoint] = []
    for i in range(0, hours * 3600, step):
        t = t0 + timedelta(seconds=i)
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        _, r, _ = satrec.sgp4(jd, fr)
        points.append(OrbitPoint(time=t, position_m=(r[0] * 1000, r[1] * 1000, r[2] * 1000)))
    return points


def broadcast_ephemeris_orbit(
    hours: int = 24,
    step: int = 60,
    base_time: datetime | None = None,
) -> list[OrbitPoint]:
    """Generate a simulated GPS broadcast ephemeris orbit."""
    t0 = _base_time(base_time)
    points: list[OrbitPoint] = []
    for i in range(0, hours * 3600, step):
        theta = 2 * np.pi * i / (hours * 3600)
        points.append(
            OrbitPoint(
                time=t0 + timedelta(seconds=i),
                position_m=(GPS_SEMI_MAJOR_AXIS_M * np.cos(theta), GPS_SEMI_MAJOR_AXIS_M * np.sin(theta), 0.0),
            )
        )
    return points


def precise_ephemeris_orbit(
    hours: int = 24,
    step: int = 60,
    base_time: datetime | None = None,
) -> list[OrbitPoint]:
    """Generate a simulated SP3 precise ephemeris orbit."""
    t0 = _base_time(base_time)
    points: list[OrbitPoint] = []
    for i in range(0, hours * 3600, step):
        theta = 2 * np.pi * i / (hours * 3600) + 0.1
        points.append(
            OrbitPoint(
                time=t0 + timedelta(seconds=i),
                position_m=(
                    PRECISE_SEMI_MAJOR_AXIS_M * np.cos(theta),
                    PRECISE_SEMI_MAJOR_AXIS_M * np.sin(theta),
                    100e3,
                ),
            )
        )
    return points
