import curses
from typing import List
from ..Entry import Entry
from ..Types import WindowGeometry
from .DefaultWindow import DefaultWindow


class FileWindow(DefaultWindow):
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
            return text
        except UnicodeDecodeError:
            self.error = "Bad encoding"
        except PermissionError:
            self.error = "Permission denied"
        except:
            pass

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
