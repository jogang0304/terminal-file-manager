from typing import Optional
from .InfoBar import InfoBar
from ..Entry import Entry
from ..Types import WindowGeometry
import os


class BottomInfoBar(InfoBar):
    def __init__(self, geometry: WindowGeometry, border: bool = False) -> None:
        super().__init__(geometry, border)

    def update_entry_info(self, entry: Optional[Entry]):
        if not entry:
            self.left_info = ""
            self.right_info = ""
        else:
            left_part = "Permissions: "
            if os.access(entry.path, os.R_OK):
                left_part += "R"
            if os.access(entry.path, os.W_OK):
                left_part += "W"
            if os.access(entry.path, os.X_OK):
                left_part += "X"
            right_part = f"Size: {entry.size} bytes"
            self.left_info = left_part
            self.right_info = right_part
        self._update_info()

    def update_output(self, text: str):
        self.mid_info = text
        self._update_info()
