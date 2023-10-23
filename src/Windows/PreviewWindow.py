from typing import Optional

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
            return
        if entry.type == EntryType.FOLDER:
            self.content = FolderWindow(self.geometry, entry.path)
        else:
            self.content = DefaultWindow(self.geometry)
