"""
The `MainScreen` class represents a window with various components for navigating and interacting
with files and folders.
"""
import curses
import os
from pathlib import Path
import tempfile
from .entry import Entry, EntryType

from .Windows.creation_window import CreateType, CreationWindow

from .FilesActions.file_processor import FilesProcessor
from .InfoBars.bottom_info_bar import BottomInfoBar
from .InfoBars.top_info_bar import TopInfoBar
from .Windows.folder_window import FolderWindow

from .Windows.main_folder_window import MainFolderWindow
from .Windows.preview_window import PreviewWindow

from .Windows.default_window import DefaultWindow

from .custom_types import WindowGeometry


class MainScreen(DefaultWindow):
    """
    The `MainScreen` class represents a window with various components for navigating
    and interacting
    with files and folders.
    """

    def __init__(
        self,
        height: int,
        width: int,
        top: int = 0,
        left: int = 0,
        path: Path = Path(os.getcwd()),
    ) -> None:
        """The function initializes a window with specified dimensions and initializes
        various components
        within the window.

        Parameters
        ----------
        height : int
            The `height` parameter represents the height of the window.
        width : int
            The `width` parameter represents the width of the window.
        top : int, optional
            The `top` parameter represents the top position of the window. It specifies the
            number of rows from the top of the screen where the window should be placed.
        left : int, optional
            The `left` parameter is an optional integer that represents the left position
            of the window. It determines the horizontal position of the window on the screen.
            If not provided, it defaults to 0.
        path : Path
            The `path` parameter is a `Path` object that represents the directory path where the
            program is currently running. It is used to initialize the `self.path`
            attribute of the class.

        """
        self.geometry = WindowGeometry(height, width, top, left)
        super().__init__(self.geometry)
        self.path = path
        self.prev_folder = self.path.parent.absolute()
        prev_folder_width = int(self.geometry.width / 5)
        main_folder_width = int(self.geometry.width / (2.5))
        preview_width = curses.COLS - prev_folder_width - main_folder_width

        self.initialize_main_window(main_folder_width, prev_folder_width)
        self.initialize_prev_window(prev_folder_width, 0)
        self.initialize_preview_window(
            preview_width, prev_folder_width + main_folder_width
        )
        self.initialize_info_bars()
        self.files_processor = FilesProcessor()
        self.update_preview_window()

    def initialize_main_window(self, width, left):
        """The function initializes the main window with a specified width and position.

        Parameters
        ----------
        width
            The width parameter is the desired width of the main folder window.
        left
            The "left" parameter represents the horizontal position of the main window,
            measured in columns from the left edge of the screen.

        """
        main_folder_window_geometry = WindowGeometry(
            self.geometry.height - 2, width, 1, left
        )
        self.main_folder_window = MainFolderWindow(main_folder_window_geometry)
        self.main_folder_window.update_path(self.path)

    def initialize_prev_window(self, width, left):
        """The function initializes a previous folder window with a specified width and position.

        Parameters
        ----------
        width
            The `width` parameter represents the width of the previous folder window.
            It determines how wide the window will be when it is displayed on the screen.
        left
            The "left" parameter represents the horizontal position of the left edge of the
            previous folder window. It is used to determine the initial position of the
            window on the screen.

        """
        prev_folder_window_geometry = WindowGeometry(
            self.geometry.height - 2, width, 1, left
        )
        self.prev_folder_window = FolderWindow(prev_folder_window_geometry)
        self.prev_folder_window.update_path(Path(self.path).parent.absolute())

    def initialize_preview_window(self, width, left):
        """The function initializes a preview window with a specified width and position.

        Parameters
        ----------
        width
            The width parameter represents the width of the preview window. It determines
            how wide the preview window will be in terms of pixels or characters.
        left
            The "left" parameter represents the horizontal position of the left edge of the
            preview window. It determines where the preview window will be positioned
            horizontally within the main window.

        """
        preview_window_geometry = WindowGeometry(
            self.geometry.height - 2, width, 1, left
        )
        self.preview_window = PreviewWindow(preview_window_geometry)

    def initialize_info_bars(self):
        """
        The function initializes and updates the top and bottom info bars with the
        given geometry and
        path.

        """
        top_info_bar_geometry = WindowGeometry(1, self.geometry.width, 0, 0)
        self.top_info_bar = TopInfoBar(top_info_bar_geometry)
        bottom_info_bar_geometry = WindowGeometry(
            1, self.geometry.width, self.geometry.height - 1, 0
        )
        self.bottom_info_bar = BottomInfoBar(bottom_info_bar_geometry)
        self.top_info_bar.update_path(self.path)

    def update_preview_window(self):
        """
        The function updates the preview window, entry info, and output in the bottom
        info bar.
        """
        if len(self.main_folder_window.entries) > 0:
            self.selected_entry = self.main_folder_window.entries[
                self.main_folder_window.selected_entry_index
            ]
        else:
            self.selected_entry = None
        self.preview_window.update(self.selected_entry)
        self.bottom_info_bar.update_entry_info(self.selected_entry)
        self.bottom_info_bar.update_output(self.files_processor.message)

    def update(self):
        """
        The function updates the path in the main folder window, previous folder
        window, and preview window.
        """
        while not self.path.exists():
            self.path = self.path.parent
        self.main_folder_window.update_path(self.path)
        self.prev_folder_window.update_path(self.path.parent.absolute())
        self.update_preview_window()

    def go_to_path(self, new_path: Path):
        """
        The function updates various windows and variables with a new path,
        and handles exceptions by reverting to the previous path.

        Parameters
        ----------
        new_path : Path
            The `new_path` parameter is a `Path` object that represents the new path to navigate to.
        """
        try:
            self.main_folder_window.update_path(new_path)
            self.prev_folder_window.update_path(new_path.parent.absolute())
            self.update_preview_window()
            self.path = new_path
            self.prev_folder = new_path.parent.absolute()
            self.top_info_bar.update_path(self.path)
        except:
            self.main_folder_window.update_path(self.path)
            self.prev_folder_window.update_path(self.prev_folder)
            self.update_preview_window()

    def go_to_prev_folder(self):
        """The function "go_to_prev_folder" navigates to the previous folder."""
        self.go_to_path(self.prev_folder)

    def go_to_selected_folder(self):
        """The function checks if a selected entry is a directory and if so,
        navigates to that directory."""
        if self.selected_entry and self.selected_entry.path.is_dir():
            self.go_to_path(self.selected_entry.path)

    def select_down(self):
        """The function selects the next item in the main folder window and updates
        the preview window."""
        self.main_folder_window.select_down()
        self.update_preview_window()

    def select_up(self):
        """The function selects the previous item in the main folder window and updates
        the preview window."""
        self.main_folder_window.select_up()
        self.update_preview_window()

    def copy(self):
        """The `copy` function copies the selected entry using the `files_processor`
        and then updates the state.
        """
        if self.selected_entry:
            self.files_processor.copy(self.selected_entry)
            self.update()

    def cut(self):
        """The function cuts the selected entry using the files processor and updates the state."""
        if self.selected_entry:
            self.files_processor.cut(self.selected_entry)
            self.update()

    def paste(self):
        """The `paste` function calls the `paste` method of the `files_processor` object,
        updates the state, and returns nothing.
        """
        self.files_processor.paste(self.path)
        self.update()

    def delete(self):
        """The function deletes the selected entry and moves it to a temporary folder."""
        if self.selected_entry:
            trash_folder = Path(tempfile.gettempdir()).joinpath("python_tfm_folder/")
            if not trash_folder.exists():
                trash_folder.mkdir()
            self.files_processor.delete(self.selected_entry, trash_folder)
            self.update()

    def undo(self):
        """
        The `undo` function calls the `undo` method of the `files_processor` object
        and then updates the state.
        """
        self.files_processor.undo()
        self.update()

    def _create(self, what_to_create: EntryType):
        """The function creates a new folder or file based on the user's input and
        updates the current state.

        Parameters
        ----------
        what_to_create : EntryType
            The parameter "what_to_create" is of type "EntryType".

        """
        create_type = (
            CreateType.FOLDER if what_to_create == EntryType.FOLDER else CreateType.FILE
        )
        creation_window = CreationWindow(self.geometry, create_type)
        name = creation_window.filename
        to_create = Entry(Path(self.path).joinpath(f"{name}/"), what_to_create)
        self.files_processor.create(to_create)
        del creation_window
        self.update()

    def create_folder(self):
        """The function creates a folder."""
        self._create(EntryType.FOLDER)

    def create_file(self):
        """The function creates a text file."""
        self._create(EntryType.TEXT)

    def open(self):
        """The function opens the selected entry using the files_processor."""
        if self.selected_entry:
            self.files_processor.open(self.selected_entry)
