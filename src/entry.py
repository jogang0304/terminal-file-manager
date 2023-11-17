"""
The `Entry` class represents a file or directory entry with properties such as
path, name, type, and size int bytes.
"""
from enum import IntEnum
import os
from pathlib import Path
import platform


class EntryType(IntEnum):
    """
    The class `EntryType` is an enumeration that represents different types of entries, such as
    executables, folders, text files, encoded files, and other types.
    """

    EXECUTABLE = 1
    FOLDER = 2
    TEXT = 3
    ENCODED = 4
    OTHER = 5


class Entry:
    """
    The `Entry` class initializes an object with properties such as
    path, name, type, and size based on the given path.
    """

    def __init__(self, path: Path, entry_type: EntryType = EntryType.TEXT) -> None:
        """The function initializes an object with properties such as
        path, name, type, and size based on the given path.

        Parameters
        ----------
        path : Path
            The `path` parameter is a `Path` object that represents the file or directory path.
            It is used to initialize the `path` attribute of the class instance.

        """
        self.path = path
        self.name = path.name
        self.type = entry_type
        if path.is_dir():
            self.type = EntryType.FOLDER
        elif self.is_executable():
            self.type = EntryType.EXECUTABLE
        try:
            self.size = os.path.getsize(path)
        except os.error:
            self.size = 0
            
    
    def is_executable(self) -> bool:
        if not self.path.is_file():
            return False
        answer = False
        if platform.system() == "Windows":
            if self.path.suffix == ".exe":
                answer = True
        else:
            if os.access(self.path, os.X_OK):
                answer = True
        return answer
