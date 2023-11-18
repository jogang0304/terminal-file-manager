"""
The `DefaultWindow` class represents a window with a specified geometry and an optional border.
"""
import curses

from src.custom_types import WindowGeometry


class DefaultWindow:
    """
    The `DefaultWindow` class represents a window with a specified geometry and an optional border.
    """

    def __init__(self, geometry: WindowGeometry, border: bool = True) -> None:
        """The function initializes a new window with a specified geometry and optional border.

        Parameters
        ----------
        geometry : WindowGeometry
            The `geometry` parameter is an instance of the `WindowGeometry` class.
            It represents the size and position of the window on the screen.
        border : bool, optional
            The `border` parameter is a boolean value that determines whether or
            not to draw a border around the window.
        """
        self.geometry = geometry
        self.window = curses.newwin(
            geometry.height, geometry.width, geometry.top, geometry.left
        )
        self._border = border
        self.draw_border()
        self.window.refresh()

    def draw_border(self):
        """
        The function draws a border around a window if the border flag is set.
        """
        if self._border:
            self.window.border()
