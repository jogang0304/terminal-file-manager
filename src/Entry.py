from enum import IntEnum
import os
from pathlib import Path


class EntryType(IntEnum):
    EXECUTABLE = 1
    FOLDER = 2
    TEXT = 3
    ENCODED = 4
    OTHER = 5


# The `Entry` class initializes an object with properties such as path, name, type, and size based on the given path.
class Entry:
    def __init__(self, path: Path, entry_type: EntryType = EntryType.TEXT) -> None:
        """The function initializes an object with properties such as path, name, type, and size based on
        the given path.

        Parameters
        ----------
        path : Path
            The `path` parameter is a `Path` object that represents the file or directory path. It is used to initialize the `path` attribute of the class instance.

        """
        self.path = path
        self.name = path.name
        self.type = entry_type
        if path.is_dir():
            self.type = EntryType.FOLDER
        elif os.access(path, os.X_OK):
            self.type = EntryType.EXECUTABLE
        try:
            self.size = os.path.getsize(path)
        except os.error:
            self.size = 0
