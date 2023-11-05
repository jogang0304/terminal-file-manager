"""
The `TopInfoBar` class is a subclass of `InfoBar` that represents a top
information bar where the working path is written.
"""
from pathlib import Path

from src.InfoBars.info_bar import InfoBar

from src.entry import EntryType
from src.custom_types import WindowGeometry


class TopInfoBar(InfoBar):
    """
    The `TopInfoBar` class is a subclass of `InfoBar` that represents a top
    information bar where the working path is written.
    """

    def __init__(self, geometry: WindowGeometry, border: bool = False) -> None:
        super().__init__(geometry, border)
        self.left_info = ""

    def update_path(self, path: Path):
        """
        The function updates the left_info attribute with the absolute path of a given folder.

        Parameters
        ----------
        path : Path
            The `path` parameter is of type `Path`, which represents a file or a
            directory path in the file system.

        """
        self.left_info = str(path.absolute())
        self._update_info(EntryType.FOLDER)
