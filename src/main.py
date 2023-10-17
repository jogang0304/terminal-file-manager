import curses
from typing import Type

from .Entry import EntryType
from .MainScreen import MainScreen


def initialize_colors():
    curses.start_color()
    curses.init_pair(100, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(EntryType.EXECUTABLE, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(EntryType.FOLDER, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(EntryType.TEXT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(EntryType.ENCODED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(EntryType.OTHER, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(101, curses.COLOR_WHITE, curses.COLOR_RED)


def main(stdscr):
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
        elif key == "KEY_LEFT":
            main_screen.go_to_prev_folder()
        elif key == "KEY_DOWN":
            main_screen.select_down()
        elif key == "KEY_UP":
            main_screen.select_up()
        elif key == "KEY_RIGHT":
            main_screen.go_to_selected_folder()
