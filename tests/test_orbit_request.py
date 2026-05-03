from datetime import datetime, timezone

import pytest
from pytestqt.qtbot import QtBot

from gui.orbit_config import OrbitConfig
from gui.server_config import ServerConfig
from gui.tle_input import TLEInput
from src.orbit.request import OrbitRequest, ServerEndpoint
from src.satellites import get_default_satellite


def test_orbit_request_validates_and_normalizes_query_types() -> None:
    request = OrbitRequest.from_query(types="state_vector,tle", base_time=datetime(2026, 1, 1, tzinfo=timezone.utc))

    assert request.types == ("state_vector", "tle")
    assert request.satellite == get_default_satellite()

    with pytest.raises(ValueError, match="Unknown orbit type"):
        OrbitRequest.from_query(types="state_vector,invalid")


def test_gui_widgets_assemble_domain_request_and_endpoint(qtbot: QtBot) -> None:
    orbit_config = OrbitConfig()
    tle_input = TLEInput()
    server_config = ServerConfig()
    qtbot.addWidget(orbit_config)
    qtbot.addWidget(tle_input)
    qtbot.addWidget(server_config)

    orbit_config._cb_precise.setChecked(False)
    request = orbit_config.get_orbit_request(tle_input.get_satellite())
    endpoint = server_config.get_endpoint()

    assert isinstance(request, OrbitRequest)
    assert request.types == ("state_vector", "tle", "broadcast")
    assert request.satellite == get_default_satellite()
    assert endpoint == ServerEndpoint(host="127.0.0.1", port=8000)
