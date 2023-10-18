from enum import IntEnum
import os
from pathlib import Path


class EntryType(IntEnum):
    EXECUTABLE = 1
    FOLDER = 2
    TEXT = 3
    ENCODED = 4
    OTHER = 5


# size в байтах
class Entry:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.type = EntryType.TEXT
        if path.is_dir():
            self.type = EntryType.FOLDER
        elif os.access(path, os.X_OK):
            self.type = EntryType.EXECUTABLE
        try:
            self.size = os.path.getsize(path)
        except os.error:
            self.size = 0
