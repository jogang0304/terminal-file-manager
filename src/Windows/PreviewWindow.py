from pathlib import Path
from typing import Optional

from .FileWindow import FileWindow

from ..Entry import Entry, EntryType

from ..Types import WindowGeometry

from .DefaultWindow import DefaultWindow

from .FolderWindow import FolderWindow


class PreviewWindow(DefaultWindow):
    def __init__(self, geometry: WindowGeometry):
        super().__init__(geometry)
        self.content = None
        pass

    def update(self, entry: Optional[Entry]):
        if not entry:
            self.content = DefaultWindow(self.geometry)
            return
        if entry.type == EntryType.FOLDER:
            self.content = FolderWindow(self.geometry, entry.path)
        else:
            self.content = FileWindow(self.geometry, entry)
