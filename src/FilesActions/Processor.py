from enum import IntEnum
from optparse import Option
import os
import shutil
from pathlib import Path
from typing import List, Optional

from ..Entry import Entry


class ActionType(IntEnum):
    COPY = 1
    PASTE = 2
    DELETE = 3
    CUT = 4


class Action:
    """
    A class which describes a file action (copy, paste, delete, cur) and is possible to revert it
    """

    def __init__(self, action_type=None, source=None, destination=None):
        self.type: Optional[ActionType] = action_type
        self.source: Optional[Path] = source
        self.destination: Optional[Path] = destination

    def undo(self) -> str:
        if self.type == ActionType.PASTE and self.destination:
            try:
                os.remove(self.destination)
                return f"Removed {self.destination}"
            except:
                return f"Error: can't remove {self.destination}"
        return "Success"


class FilesProcessor:
    """
    A class that handles operations with files (copy, paste, delete, cut)
    """

    def __init__(self):
        self.message = ""
        self.actions: List[Action] = []  # stack of actions
        self.pending_action = None
        self.pending_file: Optional[Entry] = None

    def copy(self, file: Entry):
        self.pending_action = ActionType.COPY
        self.pending_file = file
        self.message = f"Copied {file.name}"

    def paste(self, path: Path):
        if not path.is_dir or not self.pending_file:
            return
        if self.pending_action == ActionType.COPY:
            destination = shutil.copy2(self.pending_file.path, path)
            self.actions.append(
                Action(
                    ActionType.PASTE,
                    self.pending_file.path.absolute(),
                    Path(destination).absolute(),
                )
            )

    def undo(self):
        if len(self.actions) > 0:
            self.message = self.actions[-1].undo()
            self.actions.pop()
