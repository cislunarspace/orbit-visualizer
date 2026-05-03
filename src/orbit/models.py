"""Orbit domain values."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OrbitPoint:
    """A single orbit position at one instant."""

    time: datetime
    position_m: tuple[float, float, float]
