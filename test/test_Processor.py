from platform import processor
import unittest
from src.entry import Entry
from src.FilesActions.file_processor import FilesProcessor
import os
import shutil
from pathlib import Path


class TestFilesActions(unittest.TestCase):
    folder_name = "test_environment"
    testfile_name = "test1"
    testfolder_name = "test2"

    @staticmethod
    def prepare_environment():
        wd = Path(os.getcwd()).joinpath(TestFilesActions.folder_name)
        if wd.exists():
            TestFilesActions.delete_environment()
        wd.mkdir()
        with open(wd.joinpath(TestFilesActions.testfile_name), "w"):
            pass
        wd.joinpath(TestFilesActions.testfolder_name).mkdir()
        return wd

    @staticmethod
    def delete_environment():
        wd = Path(os.getcwd()).joinpath(TestFilesActions.folder_name)
        shutil.rmtree(wd)

    def test_copy(self):
        wd = self.prepare_environment()
        processor = FilesProcessor()

        processor.copy(Entry(wd.joinpath(self.testfile_name)))
        processor.paste(wd)

        expected_ls = [
            self.testfile_name,
            self.testfile_name + "(1)",
            self.testfolder_name,
        ]
        ls = os.listdir(wd)
        self.assertEqual(sorted(ls), sorted(expected_ls))

        processor.copy(Entry(wd.joinpath(self.testfolder_name)))
        processor.paste(wd.joinpath(self.testfolder_name))

        expected_ls = [self.testfolder_name]
        ls = os.listdir(wd.joinpath(self.testfolder_name))
        self.assertEqual(sorted(ls), sorted(expected_ls))

        processor.undo()
        processor.undo()

        expected_ls = [self.testfolder_name, self.testfile_name]
        ls = os.listdir(wd)
        self.assertEqual(sorted(ls), sorted(expected_ls))

        self.delete_environment()

    def test_cut(self):
        wd = self.prepare_environment()
        processor = FilesProcessor()

        processor.cut(Entry(wd.joinpath(self.testfile_name)))
        processor.paste(wd.joinpath(self.testfolder_name))

        expected_ls = [self.testfolder_name]
        ls = os.listdir(wd)
        self.assertEqual(sorted(ls), sorted(expected_ls))

        expected_ls = [self.testfile_name]
        ls = os.listdir(wd.joinpath(self.testfolder_name))
        self.assertEqual(sorted(ls), sorted(expected_ls))

        self.delete_environment()

    def test_delete(self):
        wd = self.prepare_environment()
        processor = FilesProcessor()

        processor.copy(Entry(wd.joinpath(self.testfile_name)))
        processor.paste(wd.joinpath(self.testfolder_name))
        processor.delete(Entry(wd.joinpath(self.testfile_name)))

        expected_ls = [self.testfolder_name]
        ls = os.listdir(wd)
        self.assertEqual(sorted(ls), sorted(expected_ls))

        processor.delete(Entry(wd.joinpath(self.testfolder_name)))

        expected_ls = []
        ls = os.listdir(wd)
        self.assertEqual(sorted(ls), sorted(expected_ls))

        self.delete_environment()


if __name__ == "__main__":
    unittest.main()
