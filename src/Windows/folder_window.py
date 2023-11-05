"""
The `FolderWindow` class represents a window that displays the contents
of a folder and allows for navigation and interaction with the files and directories within it.
"""
from pathlib import Path
from typing import List, Optional
import curses

from src.custom_types import WindowGeometry

from src.entry import Entry
from src.Windows.default_window import DefaultWindow


class FolderWindow(DefaultWindow):
    """
    The `FolderWindow` class represents a window that displays the contents
    of a folder and allows for navigation and updates based on the current path.
    """

    def __init__(self, geometry: WindowGeometry, path: Path = Path("/")):
        """
        The function initializes an object with a given geometry and path,
        and updates the entries and window.

        Parameters
        ----------
        geometry : WindowGeometry
            The `geometry` parameter is of type `WindowGeometry` and is used to specify
            the size and position of the window.
        path : Path
            The `path` parameter is a string that represents the directory path.
            It specifies the location where the file entries will be displayed.
            By default, it is set to the root directory ("/").

        """
        super().__init__(geometry)
        self.error: Optional[str] = None
        self.path = path
        self.entries: List[Entry] = []
        self.top_entry_index = -1
        self.bottom_entry_index = -1
        self._update_entries(self.path)
        self._update_window()

    def update_path(self, path: Path):
        """The function updates the path attribute, updates the entries based on
        the new path, and updates the window.

        Parameters
        ----------
        path : Path
            The `path` parameter is a `Path` object that represents the new path to be updated.

        """
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
