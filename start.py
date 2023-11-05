"""
This code is importing the `curses` module and the `main` module from the `src` package.
"""
import curses
import src

if __name__ == "__main__":
    curses.wrapper(src.main)
