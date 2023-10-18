import curses
import os
from pathlib import Path

from .BottomInfoBar import BottomInfoBar

from .TopInfoBar import TopInfoBar

from .PreviewWindow import PreviewWindow

from .Types import WindowGeometry

from .MainFolderWindow import MainFolderWindow

from .FolderWindow import FolderWindow
from .DefaultWindow import DefaultWindow


class MainScreen(DefaultWindow):
    def __init__(
        self,
        height: int,
        width: int,
        top: int = 0,
        left: int = 0,
        path: Path = Path(os.getcwd()),
    ) -> None:
        self.geometry = WindowGeometry(height, width, top, left)
        super().__init__(self.geometry)
        self.path = path
        self.prev_folder = self.path.parent.absolute()
        prev_folder_width = int(self.geometry.width / 5)
        main_folder_width = int(self.geometry.width / (2.5))
        preview_width = curses.COLS - prev_folder_width - main_folder_width

        self.initialize_main_window(main_folder_width, prev_folder_width)
        self.initialize_prev_window(prev_folder_width, 0)
        self.initialize_preview_window(
            preview_width, prev_folder_width + main_folder_width
        )
        self.initialize_info_bars()
        self.update_preview_window()

    def initialize_main_window(self, width, left):
        main_folder_window_geometry = WindowGeometry(
            self.geometry.height - 2, width, 1, left
        )
        self.main_folder_window = MainFolderWindow(main_folder_window_geometry)
        self.main_folder_window.update_path(self.path)

    def initialize_prev_window(self, width, left):
        prev_folder_window_geometry = WindowGeometry(
            self.geometry.height - 2, width, 1, left
        )
        self.prev_folder_window = FolderWindow(prev_folder_window_geometry)
        self.prev_folder_window.update_path(Path(self.path).parent.absolute())

    def initialize_preview_window(self, width, left):
        preview_window_geometry = WindowGeometry(
            self.geometry.height - 2, width, 1, left
        )
        self.preview_window = PreviewWindow(preview_window_geometry)

    def initialize_info_bars(self):
        top_info_bar_geometry = WindowGeometry(1, self.geometry.width, 0, 0)
        self.top_info_bar = TopInfoBar(top_info_bar_geometry)
        bottom_info_bar_geometry = WindowGeometry(
            1, self.geometry.width, self.geometry.height - 1, 0
        )
        self.bottom_info_bar = BottomInfoBar(bottom_info_bar_geometry)
        self.top_info_bar.update_path(self.path)

    def update_preview_window(self):
        self.selected_entry = self.main_folder_window.entries[
            self.main_folder_window.selected_entry_index
        ]
        self.preview_window.update(self.selected_entry)
        self.bottom_info_bar.update_entry_info(self.selected_entry)

    def go_to_path(self, new_path: Path):
        try:
            self.main_folder_window.update_path(new_path)
            self.prev_folder_window.update_path(new_path.parent.absolute())
            self.update_preview_window()
            self.path = new_path
            self.prev_folder = new_path.parent.absolute()
            self.top_info_bar.update_path(self.path)
        except:
            self.main_folder_window.update_path(self.path)
            self.prev_folder_window.update_path(self.prev_folder)
            self.update_preview_window()
            pass

    def go_to_prev_folder(self):
        self.go_to_path(self.prev_folder)

    def go_to_selected_folder(self):
        if self.selected_entry.path.is_dir():
            self.go_to_path(self.selected_entry.path)

    def select_down(self):
        self.main_folder_window.select_down()
        self.update_preview_window()

    def select_up(self):
        self.main_folder_window.select_up()
        self.update_preview_window()
