"""
tests/test_rename_project.py

Purpose:
    - This does unit testing (automated testing) for 'rename-project' command
    - To check edge cases from rename_project() function in src/cli/task_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_rename_project.py"
    - [Alternatively] To execute all unit test files inside this venv:
        "python -m unittest discover -s tests"
    - To deactivate this venv after testing:
        "deactivate"

Author: Yamin Ohmar
University: University of Leicester
"""

import io
import sys
import os
import unittest
from unittest.mock import patch

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.managers import task_manager

class TestRenameProject(unittest.TestCase):

    # using a mock object
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.isPrj_exist", return_value=False)
    def test_renamePrj_data_not_loaded(self, mock_exist, mock_load):
        """[rename-project] Test 1: not proceeding if data is not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.rename_project("testing.taskpaper", "Old", "New", "rename-project")
        # making sure load_taskpaper_data() is called once but it didn't proceed
        mock_load.assert_called_once()
        mock_exist.assert_not_called()  # make sure not proceed
        self.assertNotIn("New", task_manager.loaded_taskpaper_data)

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_renamePrj_noData(self, mock_show_error, mock_load):
        """[rename-project] Test 2: no data in taskpaper but proceed to check"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.rename_project("testing.taskpaper", "Old", "New", "rename-project")
        # making sure data is loaded and proceeded with checking but project not renamed
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Old' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("New", task_manager.loaded_taskpaper_data)

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True) 
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_renamePrj_old_empty_name(self, mock_show_error, mock_load):
        """[rename-project] Test 3: old project name is empty"""
        task_manager.loaded_taskpaper_data = {"Old": []}
        task_manager.rename_project("testing.taskpaper", "", "New", "rename-project") # empty old project name
        # making sure show_error() func was called once and new project is not added 
        mock_show_error.assert_called_once_with("Error: Invalid project name(s). The name(s) cannot be empty.")
        self.assertNotIn("New", task_manager.loaded_taskpaper_data)

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_renamePrj_new_empty_name(self, mock_show_error, mock_load):
        """[rename-project] Test 4: new project name is empty"""
        task_manager.loaded_taskpaper_data = {"Old": []}
        task_manager.rename_project("file.taskpaper", "Old", "  ", "rename-project") # empty new project name
        # making sure show_error() func was called once once and new project is not added
        mock_show_error.assert_called_once_with("Error: Invalid project name(s). The name(s) cannot be empty.")
        self.assertNotIn("New", task_manager.loaded_taskpaper_data)

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_renamePrj_old_not_exist(self, mock_show_error, mock_load):
        """[rename-project] Test 5: old project does not exist"""
        task_manager.loaded_taskpaper_data = {"Other": []}
        task_manager.rename_project("testing.taskpaper", "Old", "New", "rename-project")
        # making sure isPrj_exist() is called once and new project is not added
        mock_show_error.assert_called_once_with("Error: Project 'Old' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("New", task_manager.loaded_taskpaper_data)

   # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_renamePrj_same_name(self, mock_warning, mock_load):
        """[rename-project] Test 6: new project and old project have the same name"""
        task_manager.loaded_taskpaper_data = {"Project": []}
        task_manager.rename_project("testing.taskpaper", "Project", "Project", "rename-project")
        # making sure show_warning() is called once and no changes made
        mock_warning.assert_called_once_with("Project name remains the same. No changes made.")
        self.assertIn("Project", task_manager.loaded_taskpaper_data)

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_renamePrj_new_exists(self, mock_warn, mock_load):
        """[rename-project] Test 7: new project name exists"""
        task_manager.loaded_taskpaper_data = {"Old": [], "New": []}
        task_manager.rename_project("testing.taskpaper", "Old", "New", "rename-project")
        # making sure show_warning() is called once and no changes made
        mock_warn.assert_called_once_with("Project 'New' already exists in file 'testing.taskpaper'. \nPlease choose a different name.")
        self.assertIn("Old", task_manager.loaded_taskpaper_data)
        self.assertIn("New", task_manager.loaded_taskpaper_data)

    # using mock objects for functions that is used for this testing
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("src.managers.task_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.task_manager.undo_mng.save_backup")
    def test_renamePrj_success(self, mock_backup, mock_write, mock_success, mock_load):
        """[rename-project] Test 8: project renamed successfully"""
        task_manager.loaded_taskpaper_data = {"Old": ["- Task 1"], "Another": []}

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            task_manager.rename_project("testing.taskpaper", "Old", "New", "rename-project")
            stdout_print = mock_stdout.getvalue()

        # making sure the project was renamed in memory
        self.assertIn("New", task_manager.loaded_taskpaper_data)
        self.assertNotIn("Old", task_manager.loaded_taskpaper_data)
        self.assertIn("Renaming project 'Old' to 'New' in file 'testing.taskpaper'...", stdout_print)

        # making sure helper functions (mocked functions) were called with below arguments
        mock_backup.assert_called_once_with("testing.taskpaper", "rename-project")
        mock_write.assert_called_once_with("testing.taskpaper", task_manager.loaded_taskpaper_data)
        mock_success.assert_called_once_with("Successfully renamed project 'Old' to 'New'.")

if __name__ == "__main__":
    unittest.main()
