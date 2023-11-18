"""
The `CreationWindow` class is a subclass of `DefaultWindow` that represents a window for creating
folders or files, allowing the user to input a name for the folder or file.
"""
import curses
import enum
from src.custom_types import WindowGeometry
from src.Windows.default_window import DefaultWindow


class CreateType(enum.IntEnum):
    """
    Enumerator of thing that can be created
    """

    FOLDER = 1
    FILE = 2


class CreationWindow(DefaultWindow):
    """
    The `CreationWindow` class is a subclass of `DefaultWindow` that represents
    a window for creating folders or files, allowing the user to input a name
    for the folder or file.
    """

    def __init__(
        self, geometry: WindowGeometry, create_type: CreateType = CreateType.FOLDER
    ) -> None:
        """The function initializes a new object with a modified window geometry and
        sets the create type.

        Parameters
        ----------
        geometry : WindowGeometry
            The `geometry` parameter is an instance of the `WindowGeometry` class.
            It represents the position and size of a window. It has the following attributes:
        create_type : CreateType
            The `create_type` parameter is of type `CreateType` and is an optional
            parameter with a default value of `CreateType.FOLDER`.

        """
        new_geometry = WindowGeometry(
            3,
            20,
            geometry.top + geometry.height // 2 - 1,
            geometry.left + geometry.width // 2 - 10,
        )
        super().__init__(new_geometry, True)
        self.type = create_type
        self._update_window()

    def _update_window(self):
        """The function updates the window by clearing it, drawing a border,
        getting user input for a filename, and refreshing the window.
        """
        self.window.clear()
        self.draw_border()
        self.filename = self._raw_input(0, 1)
        self.window.refresh()

    def _raw_input(self, row: int, column: int) -> str:
        """
        The `_raw_input` function takes in a row and column position,
        prompts the user for input in a curses window, and returns the user's input as a string.

        Parameters
        ----------
        row : int
            The `row` parameter represents the row number where the input prompt
            will be displayed on the screen. It is an integer value.
        column : int
            The `column` parameter in the `_raw_input` method represents the
            starting column position where the input prompt will be displayed on the screen.

        Returns
        -------
            a string.

        """
        curses.echo(True)
        self.window.addstr(
            row,
            column,
            "Folder name" if self.type == CreateType.FOLDER else "File name",
        )
        self.window.refresh()
        result = self.window.getstr(row + 1, column, 18).decode("utf8")
        curses.echo(False)
        return result
