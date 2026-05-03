"""Pure server subprocess lifecycle logic."""

from dataclasses import dataclass
import subprocess
from typing import Optional


@dataclass(frozen=True)
class ServerEvent:
    """Lifecycle event emitted by the pure server session."""

    kind: str
    message: str = ""


class ServerSession:
    """Own subprocess lifecycle without Qt dependencies."""

    def __init__(self) -> None:
        self.process: Optional[subprocess.Popen] = None
        self.host = ""
        self.port = 0
        self.stopped_by_user = False

    def start(self, host: str, port: int) -> None:
        if self.is_running():
            return
        self.host = host
        self.port = port
        self.stopped_by_user = False
        self.process = subprocess.Popen(
            ["uvicorn", "main:app", "--host", host, "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

    def stop(self) -> None:
        if not self.is_running():
            return
        self.stopped_by_user = True
        assert self.process is not None
        self.process.terminate()
        self.process.wait()
        self.process = None

    def is_running(self) -> bool:
        if self.process is None:
            return False
        return self.process.poll() is None

    def handle_output_line(self, line: str) -> ServerEvent:
        if "Uvicorn running on" in line or "Uvicorn running" in line:
            return ServerEvent(kind="started", message=f"http://{self.host}:{self.port}")
        return ServerEvent(kind="output", message=line)

    def finish_event(self) -> ServerEvent | None:
        if self.stopped_by_user or self.process is None:
            return None
        code = self.process.poll()
        if code is not None:
            return ServerEvent(kind="failed", message=f"Server exited unexpectedly with code {code}")
        return None
