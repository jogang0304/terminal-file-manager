"""
The main function creates a text-based file manager interface and handles user input to navigate
folders, select files, and perform various file operations.s
"""
import curses

from .entry import EntryType
from .main_screen import MainScreen


def initialize_colors():
    """
    The function initializes color pairs for different types of entries in a terminal interface.
    """
    curses.start_color()
    curses.init_pair(100, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(EntryType.EXECUTABLE, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(EntryType.FOLDER, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(EntryType.TEXT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(EntryType.ENCODED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(EntryType.OTHER, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(101, curses.COLOR_WHITE, curses.COLOR_RED)


def main(stdscr):
    """The above function is the main function of a Python program that creates a
    text-based file manager interface and handles user input to navigate folders
    select files, and perform various file operations.

    Parameters
    ----------
    stdscr
        The `stdscr` parameter is a reference to the standard screen object in
        the curses library. It represents the main window that is displayed on the terminal.

    """
    stdscr.clear()
    initialize_colors()
    curses.curs_set(False)
    curses.update_lines_cols()
    stdscr.refresh()
    main_screen = MainScreen(curses.LINES, curses.COLS)
    while True:
        key = stdscr.getkey()
        if key == "q":
            break
        if key in ("KEY_LEFT", "h"):
            main_screen.go_to_prev_folder()
        elif key in ("KEY_DOWN", "j"):
            main_screen.select_down()
        elif key in ("KEY_UP", "k"):
            main_screen.select_up()
        elif key in ("KEY_RIGHT", "l"):
            main_screen.go_to_selected_folder()
        elif key == "y":
            main_screen.copy()
        elif key == "c":
            main_screen.cut()
        elif key == "p":
            main_screen.paste()
        elif key == "u":
            main_screen.undo()
        elif key == "d":
            main_screen.delete()
        elif key == "f":
            main_screen.create_folder()
        elif key == "n":
            main_screen.create_file()
        elif key == "o":
            main_screen.open()
