from datetime import datetime, timezone

from main import generate_state_vector_orbit
from src.orbit.czml import orbit_paths_to_czml
from src.orbit.models import OrbitPoint


def test_state_vector_returns_orbit_points_and_czml_formatter_builds_document() -> None:
    base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)

    points = generate_state_vector_orbit(hours=1, step=1800, base_time=base_time)
    czml = orbit_paths_to_czml([("state", points, [0, 255, 255, 180])])

    assert points
    assert isinstance(points[0], OrbitPoint)
    assert czml[0]["id"] == "document"
    assert czml[1]["id"] == "state"
    assert czml[1]["position"]["epoch"] == "2026-01-01T00:00:00Z"
