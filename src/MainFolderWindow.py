from pathlib import Path

from .Types import WindowGeometry
from .FolderWindow import FolderWindow
import curses


class MainFolderWindow(FolderWindow):
    def __init__(self, geometry: WindowGeometry, path: Path = Path("/")):
        self.selected_entry_index = 0
        super().__init__(geometry, path)

    def update_path(self, path: Path):
        super().update_path(path)

    def _update_window(self):
        super()._update_window()
        if len(self.entries) > 0:
            self.selected_entry_index = min(
                self.selected_entry_index, len(self.entries) - 1
            )
            self.window.addstr(
                self.selected_entry_index + 1,
                1,
                self.entries[self.selected_entry_index].name,
                curses.color_pair(100),
            )
            self.window.refresh()

    def select_down(self):
        self.selected_entry_index = min(
            self.selected_entry_index + 1, len(self.entries) - 1
        )
        self._update_window()

    def select_up(self):
        self.selected_entry_index = max(self.selected_entry_index - 1, 0)
        self._update_window()
