"""Built-in satellite catalog used by API and GUI entry points."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Satellite:
    """Satellite identity with a two-line element set for SGP4 propagation."""

    name: str
    tle_line1: str
    tle_line2: str


_BUILTIN_SATELLITES: tuple[Satellite, ...] = (
    Satellite(
        name="ISS",
        tle_line1="1 25544U 98067A   25123.56789017  .00000012  00000-0  12345-6 0  1234",
        tle_line2="2 25544  51.6400  10.0000 0001234  10.0000  350.0000 15.48999999123456",
    ),
    Satellite(
        name="Hubble",
        tle_line1="1 20580U 90039B   25123.50000000  .00000000  00000-0  00000-0 0  9999",
        tle_line2="2 20580  28.4700 325.0000 0001234  10.0000 200.0000 15.48999999123456",
    ),
    Satellite(
        name="Starlink-1452",
        tle_line1="1 44083U 19029Q   25123.50000000  .00000000  00000-0  00000-0 0  9999",
        tle_line2="2 44083  53.0000  10.0000 0001234  10.0000 350.0000 15.50000000123456",
    ),
)


def list_builtin_satellites() -> tuple[Satellite, ...]:
    """Return the built-in satellites in display order."""
    return _BUILTIN_SATELLITES


def get_default_satellite() -> Satellite:
    """Return the default satellite used by backend and GUI presets."""
    return _BUILTIN_SATELLITES[0]


def get_satellite(name: str) -> Satellite:
    """Return a built-in satellite by display name."""
    for satellite in _BUILTIN_SATELLITES:
        if satellite.name == name:
            return satellite
    raise KeyError(f"Unknown satellite: {name}")
