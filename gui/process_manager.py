import subprocess
import threading

from PyQt6.QtCore import QObject, pyqtSignal

from gui.server_session import ServerSession


class ProcessManager(QObject):
    """
    Qt adapter for the FastAPI/uvicorn server subprocess lifecycle.

    Signals:
        started(str):  Emitted with the server URL when server is ready.
        stopped():    Emitted when the server exits after stop().
        failed(str):   Emitted with the error message on unexpected exit.
        output(str):   Emitted for each stdout/stderr line.
    """

    started = pyqtSignal(str)
    stopped = pyqtSignal()
    failed = pyqtSignal(str)
    output = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._session = ServerSession()
        self._reader_thread: threading.Thread | None = None

    def start(self, host: str, port: int) -> None:
        if self.is_running():
            return
        self._session.start(host, port)
        self._reader_thread = threading.Thread(target=self._read_output, daemon=True)
        self._reader_thread.start()

    def stop(self) -> None:
        if not self.is_running():
            return
        self._session.stop()
        if self._reader_thread is not None:
            self._reader_thread.join(timeout=5)
        self._reader_thread = None
        self.stopped.emit()

    def is_running(self) -> bool:
        return self._session.is_running()

    def _read_output(self) -> None:
        process = self._session.process
        if process is None or process.stdout is None:
            return
        for raw_line in process.stdout:
            line = raw_line.rstrip("\n\r")
            self.output.emit(line)
            event = self._session.handle_output_line(line)
            if event.kind == "started":
                self.started.emit(event.message)
        event = self._session.finish_event()
        if event is not None and event.kind == "failed":
            self.failed.emit(event.message)
