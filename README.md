# terminal-file-manager

## About

A terminal file manager written in python. It uses curses module for graphics and pathlib and send2trash modules to make actions with files.

## Installation

1. Clone the repository and go to the downloaded folder
2. Install all requirements from requirements.txt (```pip install -r requirements.txt```)
3. Run ``` python start.py```

## Usage

Navigate with arrows or hjkl.

Copy a file or a directory with 'y'.

Paste it with 'p'.

Cut a file or a directory with 'c'.

Delete a file or a directory with 'd'. The file is moved to trash or to temporary folder. If moved to temporary folder, it can be restored.

Create new folder with 'f'.

Create new file with 'n'.

You can undo operations with 'u'.

Open a file with 'o'.

Exit with "q".
