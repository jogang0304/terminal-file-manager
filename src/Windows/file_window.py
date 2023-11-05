"""
The `FileWindow` class represents a window that displays the contents of a file,
with error handling for bad encoding or permission denied.
"""
import curses
from typing import List
from src.entry import Entry
from src.custom_types import WindowGeometry
from src.Windows.default_window import DefaultWindow


class FileWindow(DefaultWindow):
    """
    The `FileWindow` class represents a window that displays the contents of a file,
    with error handling for bad encoding or permission denied.
    """

    def __init__(self, geometry: WindowGeometry, file: Entry) -> None:
        super().__init__(geometry)
        self.file = file
        self.error = None
        self._update_window()

    def _get_text_lines(self):
        text: List[str] = []
        try:
            with open(self.file.path, "r") as file:
                for _ in range(0, self.geometry.height - 2):
                    text.append(file.readline()[0 : self.geometry.width - 2])
        except UnicodeDecodeError:
            self.error = "Bad encoding"
        except PermissionError:
            self.error = "Permission denied"
        except:
            pass
        return text

    def _update_window(self):
        self.window.clear()
        text = self._get_text_lines()
        if text:
            for i, line in enumerate(text):
                self.window.addstr(i + 1, 1, line)
        else:
            self.window.addstr(
                1,
                1,
                self.error if self.error else "Unknown error",
                curses.color_pair(101),
            )

        self.draw_border()
        self.window.refresh()
