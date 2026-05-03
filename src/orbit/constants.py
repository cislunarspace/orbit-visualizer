"""Physical constants for orbital mechanics."""

from typing import Final

# Earth gravitational parameter (GM) in m³/s²
# Source: WGS-84 ellipsoid gravitational constant
EARTH_GRAVITATIONAL_PARAMETER: Final[float] = 398600.4418e9

# LEO orbital radius for state vector simulation in meters
LEO_ORBITAL_RADIUS_M: Final[float] = 7000e3

# GPS MEO orbit semi-major axis in meters
# GPS satellites operate at approximately 20,200 km altitude
GPS_SEMI_MAJOR_AXIS_M: Final[float] = 26560e3

# Precise ephemeris semi-major axis in meters (slightly offset for visualization separation)
PRECISE_SEMI_MAJOR_AXIS_M: Final[float] = 26600e3
