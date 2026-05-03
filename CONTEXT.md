# Context

## Domain Terms

| Term | Definition |
|------|------------|
| **Satellite** | A tracked orbiting body identified by name and a two-line element (TLE) set for SGP4 propagation. |
| **OrbitPoint** | A single point in time with a 3D position (time, pos). Returned by orbit generation functions. |
| **CZML** | Cesium Language — JSON format for describing time-dynamic 3D scenes (paths, positions, styles). |

## Bounded Contexts

- **Orbit computation** — Pure mathematical models (Keplerian, SGP4) producing `OrbitPoint` sequences from physical constants and satellite TLE data.
- **CZML formatting** — Transforms `OrbitPoint` lists into Cesium-readable CZML documents with styling.
- **API** — Thin HTTP handlers that compose orbit computation + CZML formatting.
