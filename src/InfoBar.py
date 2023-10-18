from .DefaultWindow import DefaultWindow
from .Entry import EntryType
from .Types import WindowGeometry
import curses


class InfoBar(DefaultWindow):
    def __init__(self, geometry: WindowGeometry, border: bool = False) -> None:
        super().__init__(geometry, border)
        self.info = ""

    def _update_info(self, color: int = EntryType.OTHER):
        self.window.clear()
        self.draw_border()
        self.window.addstr(
            0,
            0,
            self.info,
            curses.color_pair(color),
        )
        self.window.refresh()
