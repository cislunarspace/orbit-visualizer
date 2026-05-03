---
Status: needs-triage
---

# Orbit Architecture Deepening

## Problem Statement

The orbit visualizer works today, but key behavior is spread across shallow modules. Orbit computation returns transport-shaped dicts instead of explicit domain values, CZML formatting leaks into API handlers, built-in `Satellite` knowledge is duplicated between the API and GUI, and GUI request flow is split across ad hoc dicts and tuples. This makes the system harder to change, harder to test through stable interfaces, and harder for maintainers to navigate safely.

## Solution

Deepen the architecture around the project's existing domain language. Orbit computation should produce explicit `OrbitPoint` values behind small interfaces. CZML formatting should own CZML document assembly behind one seam. `Satellite` selection should come from one catalog. User-selected options should travel through one orbit request module from the GUI to the API. Server lifecycle behavior should move behind a pure server-session seam with a thin Qt adapter. The result is the same user-facing visualization with better locality for maintainers and more leverage for callers and tests.

## User Stories

1. As a maintainer, I want built-in `Satellite` definitions to live behind one interface, so that GUI presets and Orbit computation cannot drift.
2. As a maintainer, I want one default `Satellite` source, so that changing the built-in default updates all entry points consistently.
3. As a user, I want selecting a built-in `Satellite` in the GUI to produce the same orbit result as the backend default flow, so that preset behavior is predictable.
4. As a user, I want custom TLE input to flow through the same request shape as built-in `Satellite` selection, so that both paths behave consistently.
5. As a maintainer, I want Orbit computation to return `OrbitPoint` values instead of raw transport dicts, so that the domain shape is explicit and reusable.
6. As a maintainer, I want the state-vector path to prove the deepened architecture first, so that later orbit sources can follow a working vertical slice.
7. As a maintainer, I want CZML formatting to live behind one seam, so that packet assembly rules are changed in one place.
8. As a maintainer, I want API handlers to delegate to Orbit computation and CZML formatting modules, so that the API layer stays thin.
9. As a user, I want the state-vector visualization to keep working after the refactor, so that architecture improvement does not remove current functionality.
10. As a maintainer, I want one orbit request module to represent orbit type selection, timing inputs, radius override, and `Satellite` choice, so that request validation is not scattered.
11. As a user, I want GUI configuration choices to map cleanly to backend behavior, so that the controls I set are the controls the system uses.
12. As a maintainer, I want validation for orbit request inputs to live behind one interface, so that invalid combinations are handled consistently.
13. As a maintainer, I want the TLE path to reuse the same deep modules as the state-vector path, so that new behavior does not fork the architecture again.
14. As a user, I want TLE visualization to keep working for both built-in and custom `Satellite` inputs, so that refactoring does not narrow what I can visualize.
15. As a maintainer, I want broadcast ephemeris and precise ephemeris to act as adapters behind the same Orbit computation seam, so that all orbit sources share one mental model.
16. As a user, I want combined visualization to include only the selected orbit sources, so that the request interface controls the rendered CZML consistently.
17. As a maintainer, I want server lifecycle behavior to be testable without importing the full GUI graph, so that failures in process control are easy to isolate.
18. As a user, I want start, stop, running, and failed server states to behave the same after the lifecycle refactor, so that the desktop workflow remains familiar.
19. As a maintainer, I want tests to target stable interfaces instead of widget internals and handler-specific packet details, so that tests survive refactoring.
20. As an AFK agent, I want each architecture slice to be independently demoable, so that work can land in small, verifiable increments.

## Implementation Decisions

- Build a deep `Satellite` catalog module that owns built-in `Satellite` definitions, lookup, and default selection.
- Build a deep orbit request module that represents orbit type selection, timing parameters, radius override, and `Satellite` or custom TLE choice.
- Treat `OrbitPoint` as the core domain value returned from Orbit computation modules.
- Deepen Orbit computation incrementally, starting with the state-vector slice as the first tracer bullet.
- Build one CZML formatting module whose interface accepts named `OrbitPoint` sequences and emits browser-consumable CZML.
- Keep API behavior thin by delegating orbit selection and CZML assembly to dedicated modules rather than rebuilding shapes in handlers.
- Implement the TLE path as an adapter behind the shared Orbit computation seam, consuming the shared `Satellite` catalog and orbit request module.
- Implement broadcast ephemeris and precise ephemeris as adapters behind the same Orbit computation seam.
- Build a pure server-session module for subprocess lifecycle and readiness detection, then adapt it into Qt behavior with a thin adapter.
- Preserve current user-facing behavior wherever possible while moving knowledge behind smaller, more durable interfaces.
- Ship the work as vertical slices so each completed slice is independently verifiable before the next orbit source moves onto the seam.

## Testing Decisions

- Good tests should verify observable behavior at the interface: `Satellite` lookup behavior, orbit request validation and mapping, `OrbitPoint` generation, CZML output shape, and server lifecycle transitions.
- Tests should avoid coupling to implementation details such as widget private fields, handler-owned packet assembly, or internal helper sequencing.
- The `Satellite` catalog module should have direct tests that prove built-in and default selection behavior.
- The orbit request module should have tests for valid and invalid combinations of orbit type selection, timing inputs, and `Satellite` / custom TLE inputs.
- The state-vector slice should have tests that exercise Orbit computation through `OrbitPoint` outputs and CZML formatting through its public interface.
- The TLE slice should have end-to-end tests that prove a built-in or custom `Satellite` produces the expected visualization path through shared interfaces.
- Broadcast ephemeris and precise ephemeris should have end-to-end tests through the shared Orbit computation and CZML formatting seams.
- The server-session seam should have tests for start, stop, running, and failure transitions without importing the full GUI graph.
- Existing FastAPI endpoint tests provide prior art for browser-facing API behavior, and existing GUI lifecycle tests provide prior art for preserving user-visible desktop behavior.

## Out of Scope

- Adding new orbit source types beyond state vector, TLE, broadcast ephemeris, and precise ephemeris
- Downloading live satellite catalogs or external TLE feeds
- Replacing the browser-based visualization surface with an embedded desktop renderer
- Reworking the visual design of the GUI beyond what is required to adopt the new seams
- Changing the physical models used for current orbit generation beyond interface-driven refactoring

## Further Notes

- No ADRs were present for this area during review, so the PRD assumes these deepening opportunities do not contradict recorded decisions.
- The current environment also exposes a testability gap: the checked-in virtual environment is broken and the default interpreter is missing required packages, which reinforces the value of deeper, more isolated modules.
- The architecture work is intentionally sequenced so the state-vector slice establishes the pattern before the remaining orbit sources move behind the same seam.
