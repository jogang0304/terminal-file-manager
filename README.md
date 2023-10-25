# terminal-file-manager

## About

A terminal file manager written in python. It uses curses module for graphics and pathlib and send2trash modules to make actions with files.

## Installation

1. Clone the repository and go to downloaded folder
2. install all requirements from requirements.txt (```pip install -r requrements.txt```)
3. run ``` python start.pyy```

## Usage

Navigate with arrows or hjkl.

Copy a file or a directory with 'y'.

Paste it with 'p'.

Cut a file or a directory with 'c'.

You can undo paste operation with 'u'.

Delete a file or a directory with 'd'. The file is moved to trash. Can't be undone yet.