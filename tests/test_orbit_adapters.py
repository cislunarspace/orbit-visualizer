from datetime import datetime, timezone

from src.orbit.adapters import (
    broadcast_ephemeris_orbit,
    precise_ephemeris_orbit,
    tle_satellite_orbit,
)
from src.orbit.czml import orbit_paths_to_czml
from src.orbit.models import OrbitPoint
from src.satellites import Satellite, get_default_satellite


def test_tle_adapter_accepts_builtin_and_custom_satellites_through_shared_seam() -> None:
    base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    builtin = get_default_satellite()
    custom = Satellite(name="Custom", tle_line1=builtin.tle_line1, tle_line2=builtin.tle_line2)

    builtin_points = tle_satellite_orbit(builtin, hours=1, step=3600, base_time=base_time)
    custom_points = tle_satellite_orbit(custom, hours=1, step=3600, base_time=base_time)
    czml = orbit_paths_to_czml([("TLE", custom_points, [255, 255, 0, 180])])

    assert isinstance(builtin_points[0], OrbitPoint)
    assert custom_points[0].position_m == builtin_points[0].position_m
    assert czml[1]["id"] == "TLE"


def test_ephemeris_adapters_render_through_shared_czml_formatter() -> None:
    base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)

    broadcast = broadcast_ephemeris_orbit(hours=1, step=3600, base_time=base_time)
    precise = precise_ephemeris_orbit(hours=1, step=3600, base_time=base_time)
    czml = orbit_paths_to_czml(
        [
            ("broadcast", broadcast, [0, 255, 0, 180]),
            ("precise", precise, [255, 0, 0, 180]),
        ]
    )

    assert isinstance(broadcast[0], OrbitPoint)
    assert isinstance(precise[0], OrbitPoint)
    assert [packet["id"] for packet in czml[1:]] == ["broadcast", "precise"]
