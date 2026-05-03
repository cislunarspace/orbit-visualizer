import subprocess
import threading
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal


class ProcessManager(QObject):
    """
    Manages the FastAPI/uvicorn server subprocess lifecycle.

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
        self._process: Optional[subprocess.Popen] = None
        self._reader_thread: Optional[threading.Thread] = None
        self._host: str = ""
        self._port: int = 0
        self._stopped_by_user: bool = False
        self._reader_ready: bool = False

    def start(self, host: str, port: int) -> None:
        if self.is_running():
            return
        self._stopped_by_user = False
        self._host = host
        self._port = port
        self._process = subprocess.Popen(
            ["uvicorn", "main:app", "--host", host, "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self._reader_thread = threading.Thread(target=self._read_output, daemon=True)
        self._reader_thread.start()

    def stop(self) -> None:
        if not self.is_running():
            return
        self._stopped_by_user = True
        assert self._process is not None
        self._process.terminate()
        self._process.wait()
        if self._reader_thread is not None:
            self._reader_thread.join(timeout=5)
        self._process = None
        self._reader_thread = None
        self.stopped.emit()

    def is_running(self) -> bool:
        if self._process is None:
            return False
        return self._process.poll() is None

    def _read_output(self) -> None:
        process = self._process
        if process is None:
            return
        for raw_line in process.stdout:
            line = raw_line.rstrip("\n\r")
            self.output.emit(line)
            if "Uvicorn running on" in line or "Uvicorn running" in line:
                self.started.emit(f"http://{self._host}:{self._port}")
        # Thread finished — check if unexpected exit
        if not self._stopped_by_user:
            code = process.poll()
            if code is not None:
                self.failed.emit(f"Server exited unexpectedly with code {code}")
