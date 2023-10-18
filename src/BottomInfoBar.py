from .InfoBar import InfoBar
from .Entry import Entry
from .Types import WindowGeometry
from .DefaultWindow import DefaultWindow
import os


class BottomInfoBar(InfoBar):
    def __init__(self, geometry: WindowGeometry, border: bool = False) -> None:
        super().__init__(geometry, border)

    def update_entry_info(self, entry: Entry):
        left_part = "Permissions: "
        if os.access(entry.path, os.R_OK):
            left_part += "R"
        if os.access(entry.path, os.W_OK):
            left_part += "W"
        if os.access(entry.path, os.X_OK):
            left_part += "X"
        right_part = f"Size: {entry.size} bytes"
        self.info = (
            left_part
            + " " * (self.geometry.width - 1 - len(left_part) - len(right_part))
            + right_part
        )
        self._update_info()
