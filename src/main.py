import curses
from typing import Type

from .Entry import EntryType
from .MainScreen import MainScreen


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
    """The above function is the main function of a Python program that creates a text-based file manager interface and handles user input to navigate folders, select files, and perform various file operations.

    Parameters
    ----------
    stdscr
        The `stdscr` parameter is a reference to the standard screen object in the curses library. It represents the main window that is displayed on the terminal.

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
        elif key == "KEY_LEFT" or key == "h":
            main_screen.go_to_prev_folder()
        elif key == "KEY_DOWN" or key == "j":
            main_screen.select_down()
        elif key == "KEY_UP" or key == "k":
            main_screen.select_up()
        elif key == "KEY_RIGHT" or key == "l":
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
