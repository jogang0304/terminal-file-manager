"""
The `MainFolderWindow` class is a subclass of `FolderWindow`. It is a central window,
with which user interacts.
"""
from pathlib import Path

from src.custom_types import WindowGeometry
from src.Windows.folder_window import FolderWindow


class MainFolderWindow(FolderWindow):
    """
    The `MainFolderWindow` class is a subclass of `FolderWindow`. It is a central window,
    with which user interacts.
    """

    def __init__(self, geometry: WindowGeometry, path: Path = Path("/")):
        self.selected_entry_index = 0
        super().__init__(geometry, path)

    def _update_window(self):
        super()._update_window()
        if len(self.entries) > 0:
            self.selected_entry_index = min(
                self.selected_entry_index, len(self.entries) - 1
            )
            self._display_entry_by_index(self.selected_entry_index, 100)
            self.window.refresh()

    def select_down(self):
        """The function selects the next entry in a list and updates the
        window display accordingly."""
        self.selected_entry_index = min(
            self.selected_entry_index + 1, len(self.entries) - 1
        )
        if self.selected_entry_index > self.bottom_entry_index:
            self.top_entry_index += 1
            self.bottom_entry_index += 1
        self._update_window()

    def select_up(self):
        """The function selects the previous entry in a list and updates
        the window display accordingly."""
        self.selected_entry_index = max(self.selected_entry_index - 1, 0)
        if self.selected_entry_index < self.top_entry_index:
            self.top_entry_index -= 1
            self.bottom_entry_index -= 1
        self._update_window()
