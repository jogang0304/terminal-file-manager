from ..Windows.DefaultWindow import DefaultWindow
from ..Entry import EntryType
from ..Types import WindowGeometry
import curses


class InfoBar(DefaultWindow):
    def __init__(self, geometry: WindowGeometry, border: bool = False) -> None:
        super().__init__(geometry, border)
        self.left_info = ""
        self.right_info = ""
        self.mid_info = ""

    def _update_info(self, color: int = EntryType.OTHER):
        self.window.clear()
        self.draw_border()
        free_space = (
            self.geometry.width
            - len(self.left_info)
            - len(self.right_info)
            - len(self.mid_info)
        )
        gap = free_space // 2
        self.window.addstr(
            0,
            0,
            self.left_info,
            curses.color_pair(color),
        )
        self.window.addstr(
            0,
            len(self.left_info) + gap,
            self.mid_info,
            curses.color_pair(color),
        )
        self.window.addstr(
            0,
            len(self.left_info) + len(self.mid_info) + 2 * gap - 1,
            self.right_info,
            curses.color_pair(color),
        )
        self.window.refresh()
