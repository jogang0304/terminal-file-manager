"""
The `BottomInfoBar` class is a subclass of `InfoBar` that displays information
about a file or directory entry at the bottom of a window.
"""
import os
from typing import Optional
from src.InfoBars.info_bar import InfoBar
from src.entry import Entry
from src.custom_types import WindowGeometry


class BottomInfoBar(InfoBar):
    """
    The `BottomInfoBar` class is a subclass of `InfoBar` that displays information
    about a file or directory entry at the bottom of a window.
    """

    def __init__(self, geometry: WindowGeometry, border: bool = False) -> None:
        super().__init__(geometry, border)
        self.left_info = ""
        self.right_info = ""
        self.mid_info = ""

    def update_entry_info(self, entry: Optional[Entry]):
        """The function updates the left and right information of an entry based on its
        permissions and size.

        Parameters
        ----------
        entry : Optional[Entry]

        """
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
        """The function updates the `mid_info` attribute with the provided `text` and then calls the
        `_update_info()` method.

        Parameters
        ----------
        text : str
            The `text` parameter is a string that represents the updated
            information that needs to be displayed.

        """
        self.mid_info = text
        self._update_info()
