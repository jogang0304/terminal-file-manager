from pathlib import Path

from .InfoBar import InfoBar

from ..Entry import EntryType
from ..Windows.DefaultWindow import DefaultWindow
from ..Types import WindowGeometry
import curses


class TopInfoBar(InfoBar):
    def __init__(self, geometry: WindowGeometry, border: bool = False) -> None:
        super().__init__(geometry, border)

    def update_path(self, path: Path):
        self.left_info = str(path.absolute())
        self._update_info(EntryType.FOLDER)
