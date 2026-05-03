"""Built-in help dialog with full user manual."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget


class HelpDialog(QDialog):
    """Modal help dialog showing the full user manual."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("帮助 / Help")
        self.setMinimumSize(700, 500)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)

        content_layout.addWidget(self._make_section(
            "卫星轨道可视化器 — 用户手册",
            [
                "本应用程序用于在三维地球上可视化多种卫星轨道。",
                "",
                "【启动】",
                "运行 `uv run python -m gui` 启动 GUI 控制面板。服务器将在后台自动启动并打开浏览器。",
                "",
                "【轨道类型】",
                "• 状态向量 — 仿真圆轨道，用于演示和教学",
                "• TLE — 基于两行根数(TLE)的 SGP4 真实卫星轨道预报",
                "• 广播星历 — 模拟 GPS 导航卫星轨道",
                "• 精密星历 — 模拟科学级精密星历",
                "",
                "取消选中某种轨道类型，可视化中将不显示该轨道。",
                "",
                "【轨道参数】",
                "• 投影时长 — 轨道投影的总时间范围（小时）",
                "• 时间步长 — 相邻轨道点之间的时间间隔（秒）",
                "• 起始时间 — 轨道投影的起始时刻（UTC）",
                "• 轨道半径 — 状态向量轨道的参考轨道半径（米）",
                "",
                "【TLE 输入】",
                "TLE（两行根数）是描述卫星轨道的标准化格式。",
                "支持预设卫星：ISS（国际空间站）、Hubble（哈勃望远镜）、Starlink-1452（星链1452）。",
                "选择 Custom 可手动输入任意卫星的 TLE 数据。",
                "TLE 数据会随时间衰减，建议使用 30 天以内的 TLE 以获得准确预报。",
                "TLE 数据可从 Space-Track.org 或 Celestrak.org 获取。",
                "",
                "【服务器配置】",
                "默认主机 127.0.0.1，端口 8000。若端口被占用，请更换端口后重新启动。",
                "",
                "【状态栏】",
                "• 已停止 — 服务器未运行",
                "• 启动中 — 服务器正在启动",
                "• 运行中 — 服务器已就绪，可点击「打开浏览器 →」打开可视化页面",
                "• 启动失败 — 服务器启动失败，请检查端口是否被占用",
                "",
                "【关闭窗口】",
                "关闭窗口时，若服务器正在运行，将自动停止服务器。",
            ]
        ))

        content_layout.addWidget(self._make_section(
            "Satellite Orbit Visualizer — User Manual",
            [
                "This application visualizes multiple satellite orbit types on a 3D globe.",
                "",
                "[Launch]",
                "Run `uv run python -m gui` to start the GUI control panel. "
                "The server starts automatically in the background and the browser opens.",
                "",
                "[Orbit Types]",
                "• State Vector — Simulated circular orbit for demos and teaching",
                "• TLE — Real satellite prediction using SGP4 propagation from two-line elements",
                "• Broadcast — Simulated GPS navigation satellite orbit",
                "• Precise — Simulated scientific-grade precise ephemeris",
                "",
                "Unchecking an orbit type hides it from the visualization.",
                "",
                "[Orbit Parameters]",
                "• Hours — Total time span for the orbit projection",
                "• Step — Time interval between consecutive orbit points (seconds)",
                "• Base Time — Starting time for the orbit projection (UTC)",
                "• Radius — Reference orbital radius for the state vector orbit (meters)",
                "",
                "[TLE Input]",
                "TLE (Two-Line Element) is a standardized format encoding satellite orbital elements.",
                "Presets: ISS (International Space Station), Hubble (Space Telescope), Starlink-1452.",
                "Select Custom to enter TLE data for any satellite manually.",
                "TLE accuracy degrades over time — use data less than 30 days old for best results.",
                "Obtain TLE data from Space-Track.org or Celestrak.org.",
                "",
                "[Server Configuration]",
                "Default host 127.0.0.1, port 8000. If the port is in use, change it and restart.",
                "",
                "[Status Bar]",
                "• Stopped — Server is not running",
                "• Starting — Server is initializing",
                "• Running — Server is ready; click 'Open Browser →' to view the visualization",
                "• Failed — Server failed to start; check if the port is in use",
                "",
                "[Closing the Window]",
                "Closing the window automatically stops the server if it is running.",
            ]
        ))

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        close_btn = QPushButton("关闭 / Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _make_section(self, title: str, lines: list[str]) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 4px 0;")
        layout.addWidget(title_label)
        for line in lines:
            lbl = QLabel(line)
            lbl.setWordWrap(True)
            lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(lbl)
        return widget
