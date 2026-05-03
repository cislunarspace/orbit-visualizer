from unittest.mock import MagicMock, patch

from gui.server_session import ServerEvent, ServerSession


def test_server_session_start_stop_and_readiness_are_pure_process_logic() -> None:
    with patch("gui.server_session.subprocess.Popen") as mock_popen:
        process = MagicMock()
        process.poll.return_value = None
        mock_popen.return_value = process

        session = ServerSession()
        session.start("127.0.0.1", 8000)
        event = session.handle_output_line("INFO: Uvicorn running on http://127.0.0.1:8000")

        assert event == ServerEvent(kind="started", message="http://127.0.0.1:8000")
        assert session.is_running() is True

        session.stop()
        process.terminate.assert_called_once()
        assert session.is_running() is False
