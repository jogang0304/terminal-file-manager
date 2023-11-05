from enum import IntEnum
from optparse import Option
import os
import platform
import shutil
from pathlib import Path
import subprocess
from typing import List, Optional
from send2trash import send2trash

from ..Entry import Entry, EntryType


class ActionType(IntEnum):
    COPY = 1
    PASTE = 2
    DELETE = 3
    CUT = 4
    CREATE = 5


class Action:
    """
    A class which describes a file action (copy, paste, delete, cur) and is possible to revert it
    """

    def __init__(
        self,
        action_type: Optional[ActionType] = None,
        source: Optional[Path] = None,
        destination: Optional[Path] = None,
    ):
        self.type: Optional[ActionType] = action_type
        self.source: Optional[Path] = source
        self.destination: Optional[Path] = destination

    def undo(self) -> str:
        """The `undo` function checks the type of action performed and undoes it by either copying the destination to the source and deleting the destination, or by deleting the source.

        Returns
        -------
            The return value depends on the conditions in the code. If the `type` is `ActionType.PASTE` and both `source` and `destination` are provided, it will try to remove the `destination` file or directory and return a string indicating success or failure. If the `type` is `ActionType.DELETE` and `source` is provided, it will do nothing.

        """
        if self.type == ActionType.PASTE and self.source and self.destination:
            try:
                if not self.source.exists():
                    if self.destination.is_dir():
                        shutil.copytree(self.destination, self.source)
                    else:
                        shutil.copy2(self.destination, self.source)

                send2trash(self.destination)
                return f"Removed {self.destination.name}"
            except:
                return f"Error: can't remove {self.destination.name}"
        elif self.type == ActionType.DELETE and self.source:
            pass
        elif self.type == ActionType.CREATE and self.source:
            try:
                send2trash(self.source)
                return f"Removed {self.source.name}"
            except:
                return f"Error: can't remove {self.source.name}"
        return "Nothing to undo"


class FilesProcessor:
    """
    A class that handles operations with files (copy, paste, delete, cut)
    """

    def __init__(self):
        self.message = ""
        self.actions: List[Action] = []  # stack of actions
        self.pending_action = None
        self.pending_file: Optional[Entry] = None

    @staticmethod
    def _get_pending_file_destination(path: Path, name: str):
        """The `_get_pending_file_destination` function returns a unique file destination path by appending a suffix to the given name if a file with the same name already exists in the given path.

        Parameters
        ----------
        path : Path
            The `path` parameter is a `Path` object representing the directory where the file will be saved.
        name : str
            The `name` parameter is a string representing the desired name of the file.

        Returns
        -------
            The method is returning the path to the pending file destination.

        """
        filename_suffix = 0
        pending_file_destination = path.joinpath(
            name + (f"({filename_suffix})" if filename_suffix else "")
        )
        while pending_file_destination.exists():
            filename_suffix += 1
            pending_file_destination = path.joinpath(
                name + (f"({filename_suffix})" if filename_suffix else "")
            )
        return pending_file_destination

    def copy(self, file: Entry):
        """The function `copy` sets the pending action to copy and stores the file to be copied.

        Parameters
        ----------
        file : Entry
            The `file` parameter is an instance of the `Entry` class.

        """
        self.pending_action = ActionType.COPY
        self.pending_file = file
        self.message = f"Copied {file.name}"

    def cut(self, file: Entry):
        """The function `cut` sets the pending action to cut and stores the file to be cut.

        Parameters
        ----------
        file : Entry
            The `file` parameter is an instance of the `Entry` class.

        """
        self.pending_action = ActionType.CUT
        self.pending_file = file
        self.message = f"Copied {file.name} for cutting"

    def paste(self, path: Path):
        """The `paste` function copies or moves a file or directory to a specified destination path and records the action in a list.

        Parameters
        ----------
        path : Path
            The `path` parameter is of type `Path` and represents the destination directory where the file or folder will be pasted.
        """
        if not path.is_dir or not self.pending_file:
            return
        if (
            self.pending_action in (ActionType.COPY, ActionType.CUT)
            and self.pending_file.path.exists()
        ):
            pending_file_destination = self._get_pending_file_destination(
                path, self.pending_file.name
            )
            if self.pending_file.path.is_dir():
                destination = shutil.copytree(
                    self.pending_file.path, pending_file_destination
                )
            else:
                destination = shutil.copy2(
                    self.pending_file.path, pending_file_destination
                )
            if self.pending_action == ActionType.CUT:
                send2trash(self.pending_file.path)
            self.actions.append(
                Action(
                    ActionType.PASTE,
                    self.pending_file.path.absolute(),
                    Path(destination).absolute(),
                )
            )

    def delete(self, file: Entry):
        """The `delete` function deletes a file and updates the message and actions list accordingly.

        Parameters
        --------
        file : Entry
            The `file` parameter is an instance of the `Entry` class. It represents a file or directory
        that you want to delete.

        """
        send2trash(file.path)
        self.message = f"Deleted {file.name}"
        self.actions.append(Action(ActionType.DELETE, file.path))

    def create(self, file: Entry):
        if file.type == EntryType.FOLDER:
            file.path.mkdir()
        else:
            file.path.touch()
        self.actions.append(Action(ActionType.CREATE, file.path))

    def undo(self):
        """The `undo` function undoes the last action performed by removing it from the list of actions and
        updating the message.

        """
        if len(self.actions) > 0:
            self.message = self.actions[-1].undo()
            self.actions.pop()

    def open(self, file: Entry):
        if file.type == EntryType.FOLDER:
            return
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(file.path)  # type: ignore
            else:
                opener = "xdg-open"
                if system == "Darwin":
                    opener = "open"
                subprocess.call(
                    (opener, file.path),
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                )
        except:
            self.message = f"Error opening {file.name}"
