"""Domain request values for orbit visualization flows."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal

from src.satellites import Satellite, get_default_satellite

OrbitType = Literal["state_vector", "tle", "broadcast", "precise"]
VALID_ORBIT_TYPES: tuple[OrbitType, ...] = ("state_vector", "tle", "broadcast", "precise")


@dataclass(frozen=True)
class OrbitRequest:
    """User-selected orbit computation inputs shared by GUI and API seams."""

    types: tuple[OrbitType, ...] = VALID_ORBIT_TYPES
    hours: int = 24
    step: int = 60
    base_time: datetime | None = None
    radius_m: float | None = None
    satellite: Satellite | None = get_default_satellite()

    def __post_init__(self) -> None:
        unknown = [orbit_type for orbit_type in self.types if orbit_type not in VALID_ORBIT_TYPES]
        if unknown:
            raise ValueError(f"Unknown orbit type: {', '.join(unknown)}")
        if self.hours <= 0:
            raise ValueError("hours must be positive")
        if self.step <= 0:
            raise ValueError("step must be positive")
        if self.satellite is None:
            object.__setattr__(self, "satellite", get_default_satellite())
        if self.base_time is not None and self.base_time.tzinfo is None:
            object.__setattr__(self, "base_time", self.base_time.replace(tzinfo=timezone.utc))

    @classmethod
    def from_query(
        cls,
        types: str | None = None,
        *,
        hours: int = 24,
        step: int = 60,
        base_time: datetime | None = None,
        radius_m: float | None = None,
        satellite: Satellite | None = None,
        ignore_unknown: bool = False,
    ) -> "OrbitRequest":
        if types:
            parts = tuple(part.strip() for part in types.split(",") if part.strip())
            requested = tuple(part for part in parts if part in VALID_ORBIT_TYPES) if ignore_unknown else parts
        else:
            requested = VALID_ORBIT_TYPES
        return cls(
            types=requested,  # type: ignore[arg-type]
            hours=hours,
            step=step,
            base_time=base_time,
            radius_m=radius_m,
            satellite=satellite or get_default_satellite(),
        )


@dataclass(frozen=True)
class ServerEndpoint:
    """Host and port used to launch the local API server."""

    host: str
    port: int
