"""
The `PreviewWindow` class is a subclass of `DefaultWindow` that displays the content 
of a selected file or folder.
"""
from typing import Optional

from src.Windows.file_window import FileWindow

from src.entry import Entry, EntryType

from src.custom_types import WindowGeometry

from src.Windows.default_window import DefaultWindow

from src.Windows.folder_window import FolderWindow


class PreviewWindow(DefaultWindow):
    """
    The `PreviewWindow` class is a subclass of `DefaultWindow` that displays the content
    of a selected file or folder."""

    def __init__(self, geometry: WindowGeometry):
        super().__init__(geometry)
        self.content = None

    def update(self, entry: Optional[Entry]):
        """The `update` function updates the content of a window based on
        the type of entry provided.

        Parameters
        ----------
        entry : Optional[Entry]
            The `entry` parameter is of type `Optional[Entry]`.

        """
        if not entry:
            self.content = DefaultWindow(self.geometry)
            return
        if entry.type == EntryType.FOLDER:
            self.content = FolderWindow(self.geometry, entry.path)
        else:
            self.content = FileWindow(self.geometry, entry)
