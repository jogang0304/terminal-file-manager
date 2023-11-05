import curses
import enum
from ..Types import WindowGeometry
from .DefaultWindow import DefaultWindow


class CreateType(enum.IntEnum):
    FOLDER = 1
    FILE = 2


class CreationWindow(DefaultWindow):
    def __init__(
        self, geometry: WindowGeometry, create_type: CreateType = CreateType.FOLDER
    ) -> None:
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
        self.window.clear()
        self.draw_border()
        self.filename = self._raw_input(0, 1)
        self.window.refresh()

    def _raw_input(self, row: int, column: int) -> str:
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
