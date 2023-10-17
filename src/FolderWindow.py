from optparse import Option
from pathlib import Path
from typing import List, Optional
import curses

from .Types import WindowGeometry

from .Entry import Entry
from .DefaultWindow import DefaultWindow
import os


class FolderWindow(DefaultWindow):

    def __init__(self, geometry: WindowGeometry, path: Path = Path("/")):
        super().__init__(geometry)
        self.error: Optional[str] = None
        self.path = path
        self.entries: List[Entry] = []
        self._update_entries(self.path)
        self._update_window()

    def update_path(self, path: Path):
        self.path = path
        self._update_entries(self.path)
        self._update_window()

    def _update_entries(self, path: Path):
        self.entries.clear()
        try:
            for child in path.iterdir():
                self.entries.append(Entry(child))
        except PermissionError:
            self.error = "Not enogh permissions"

    def _update_window(self):
        self.window.clear()
        self.draw_border()
        if len(self.entries) > 0:
            for y in range(1, min(self.geometry.height, len(self.entries) + 1)):
                entry = self.entries[y - 1]
                self.window.addstr(y, 1, entry.name, curses.color_pair(entry.type))
        else:
            self.window.addstr(
                1,
                1,
                self.error if self.error else "empty folder",
                curses.color_pair(101),
            )
        self.window.refresh()
