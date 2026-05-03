from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_api_all_filter_state_vector_only():
    """GET /api/all?types=state_vector returns only the state vector orbit."""
    response = client.get("/api/all?types=state_vector")
    assert response.status_code == 200
    packets = response.json()
    ids = [p.get("id") for p in packets]
    # document packet must be present
    assert "document" in ids
    # exactly one orbit packet: 状态向量
    orbit_ids = [i for i in ids if i != "document"]
    assert orbit_ids == ["状态向量"]


def test_api_all_filter_multiple_types():
    """GET /api/all?types=state_vector,tle returns exactly those two."""
    response = client.get("/api/all?types=state_vector,tle")
    assert response.status_code == 200
    packets = response.json()
    orbit_ids = [p.get("id") for p in packets if p.get("id") != "document"]
    assert set(orbit_ids) == {"状态向量", "TLE"}


def test_api_all_filter_broadcast_and_precise():
    """GET /api/all?types=broadcast,precise returns exactly those two."""
    response = client.get("/api/all?types=broadcast,precise")
    assert response.status_code == 200
    packets = response.json()
    orbit_ids = [p.get("id") for p in packets if p.get("id") != "document"]
    assert set(orbit_ids) == {"广播星历", "精密星历"}


def test_api_all_no_filter_returns_all_four():
    """GET /api/all with no types param returns all four orbit types."""
    response = client.get("/api/all")
    assert response.status_code == 200
    packets = response.json()
    orbit_ids = [p.get("id") for p in packets if p.get("id") != "document"]
    assert len(orbit_ids) == 4


def test_api_all_filter_invalid_type_ignored():
    """Invalid type names are silently ignored; valid types are returned."""
    response = client.get("/api/all?types=state_vector,invalid_type_xyz")
    assert response.status_code == 200
    packets = response.json()
    orbit_ids = [p.get("id") for p in packets if p.get("id") != "document"]
    assert orbit_ids == ["状态向量"]
