"""ISS (International Space Station) TLE data and Satellite domain object."""

from dataclasses import dataclass

from .tle_data import _ISS_TLE1, _ISS_TLE2


@dataclass(frozen=True)
class Satellite:
    """Satellite identity with two-line element set for SGP4 propagation."""

    name: str
    tle_line1: str
    tle_line2: str


def get_default_satellite() -> Satellite:
    """Return the default ISS TLE for orbital propagation."""
    return Satellite(name="ISS (Zarya)", tle_line1=_ISS_TLE1, tle_line2=_ISS_TLE2)
