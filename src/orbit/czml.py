"""CZML document formatting for orbit paths."""

from collections.abc import Sequence

from .models import OrbitPoint

Color = list[int]
NamedOrbitPath = tuple[str, Sequence[OrbitPoint], Color]


def utc_str(point: OrbitPoint) -> str:
    """Format an OrbitPoint timestamp for CZML."""
    return point.time.isoformat().replace("+00:00", "Z")


def orbit_path_packet(name: str, points: Sequence[OrbitPoint], color: Color) -> dict:
    """Build one CZML packet for a named orbit path."""
    if not points:
        raise ValueError("CZML orbit path requires at least one point")
    epoch = utc_str(points[0])
    return {
        "id": name,
        "name": name,
        "position": {
            "epoch": epoch,
            "cartesian": [value for point in points for value in point.position_m],
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
    }


def orbit_paths_to_czml(paths: Sequence[NamedOrbitPath]) -> list[dict]:
    """Build a browser-consumable CZML document from named orbit paths."""
    packets = [orbit_path_packet(name, points, color) for name, points, color in paths]
    all_points = [point for _, points, _ in paths for point in points]
    document: dict = {"id": "document", "version": "1.0"}
    if all_points:
        document["clock"] = {
            "interval": f"{utc_str(all_points[0])}/{utc_str(all_points[-1])}",
            "currentTime": utc_str(all_points[0]),
            "multiplier": 60,
        }
    return [document, *packets]


def single_orbit_to_czml(name: str, points: Sequence[OrbitPoint], color: Color) -> list[dict]:
    """Build a CZML document containing one orbit path."""
    return orbit_paths_to_czml([(name, points, color)])
