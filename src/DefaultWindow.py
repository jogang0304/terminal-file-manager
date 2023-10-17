import curses
from time import sleep

from .Types import WindowGeometry


class DefaultWindow:
    def __init__(self, geometry: WindowGeometry, border: bool = True) -> None:
        self.geometry = geometry
        self.window = curses.newwin(
            geometry.height, geometry.width, geometry.top, geometry.left
        )
        if border:
            self.draw_border()
        self.window.refresh()

    def draw_border(self):
        self.window.border()
