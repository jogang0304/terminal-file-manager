from pathlib import Path
from typing import List, Optional
import curses

from ..Types import WindowGeometry

from ..Entry import Entry
from .DefaultWindow import DefaultWindow


class FolderWindow(DefaultWindow):
    def __init__(self, geometry: WindowGeometry, path: Path = Path("/")):
        super().__init__(geometry)
        self.error: Optional[str] = None
        self.path = path
        self.entries: List[Entry] = []
        self.top_entry_index = -1
        self.bottom_entry_index = -1
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
            self.top_entry_index = 0
            self.bottom_entry_index = min(
                len(self.entries) - 1, self.geometry.height - 3
            )
        except PermissionError:
            self.error = "Not enogh permissions"

    def _get_name_to_display(self, entry: Entry) -> str:
        name_to_display = entry.name
        if len(name_to_display) > self.geometry.width - 2:
            name_to_display = name_to_display[0 : self.geometry.width - 5] + "..."
        return name_to_display

    def _display_entry_by_index(self, index: int, color_pair: int = -1):
        entry = self.entries[index]
        self.window.addstr(
            index - self.top_entry_index + 1,
            1,
            self._get_name_to_display(entry),
            curses.color_pair(entry.type if color_pair == -1 else color_pair),
        )

    def _update_window(self):
        self.window.clear()
        if len(self.entries) > 0:
            for i in range(self.top_entry_index, self.bottom_entry_index + 1):
                self._display_entry_by_index(i)
        else:
            self.window.addstr(
                1,
                1,
                self.error if self.error else "empty folder",
                curses.color_pair(101),
            )
        self.draw_border()
        self.window.refresh()
