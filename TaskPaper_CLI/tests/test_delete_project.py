"""
tests/test_delete_project.py

Purpose:
    - This does unit testing (automated testing) for 'delete-project' command
    - To check edge cases from delete_project() function in src/cli/task_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_delete_project.py"
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

class TestDeleteProject(unittest.TestCase):

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.isPrj_exist", return_value=False)
    def test_delPrj_data_not_loaded(self, mock_exist, mock_load):
        """[delete-project] Test 1: not proceeding if data is not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.delete_project("testing.taskpaper", "Project A", "delete-project")
        # test(s)
        mock_load.assert_called_once()
        mock_exist.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data) # make sure not in file

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_delPrj_nodata(self, mock_show_error, mock_load):
        """[delete-project] Test 2: no data in taskpaper but proceed to check"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.delete_project("testing.taskpaper", "Project A", "delete-project")
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data) # make sure not in file

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_delPrj_empty_name(self, mock_error, mock_load):
        """[delete-project] Test 3: project name is empty"""
        task_manager.loaded_taskpaper_data = {"Existing": []}
        task_manager.delete_project("testing.taskpaper", "   ", "delete-project")
        # test(s)
        mock_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertIn("Existing", task_manager.loaded_taskpaper_data)   # make sure not deleted

    @patch("src.managers.task_manager.help_mng.show_error")
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_delPrj_not_exist(self, mock_load, mock_show_error):
        """[delete-project] Test 4: project does not exist"""
        task_manager.loaded_taskpaper_data = {"Project A": []}
        task_manager.delete_project("testing.taskpaper", "Nonexistent", "delete-project")
        # test(s)
        mock_show_error.assert_called_once_with("Error: Project 'Nonexistent' does not exist in file 'testing.taskpaper'.")
        self.assertIn("Project A", task_manager.loaded_taskpaper_data)   # make sure not deleted

    # using mock objects (including standard input value mocking)
    @patch("src.managers.task_manager.help_mng.show_warning")
    @patch("src.managers.task_manager.std_input", return_value='n')
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_delPrj_cancelled(self, mock_load, mock_input, mock_warn):
        """[delete-project] Test 5: when deletion is canceled by user"""
        task_manager.loaded_taskpaper_data = {"Project A": []}
        task_manager.delete_project("testing.taskpaper", "Project A", "delete-project")
        # test(s)
        mock_warn.assert_called_once_with("Project deletion cancelled.")
        self.assertIn("Project A", task_manager.loaded_taskpaper_data)   # make sure not deleted

    # using mock objects (including standard input value mocking)
    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("src.managers.task_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.task_manager.undo_mng.save_backup")
    @patch("src.managers.task_manager.std_input", return_value='y')
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_delPrj_success(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[delete-project] Test 6: successfully delete project when user confirmed"""
        task_manager.loaded_taskpaper_data = {
            "Project A": ["Task 1"],
            "Keep Me": []
        }

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            task_manager.delete_project("testing.taskpaper", "Project A", "delete-project")
            stdout_print = mock_stdout.getvalue()
        
        # test(s)
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data) # make sure project deleted
        self.assertNotIn("Task 1", task_manager.loaded_taskpaper_data) # make sure task also deleted
        self.assertIn("Keep Me", task_manager.loaded_taskpaper_data) # make sure not deleted
        self.assertIn("Deleting the project 'Project A' in file 'testing.taskpaper'...", stdout_print)
        mock_backup.assert_called_once_with("testing.taskpaper", "delete-project") # make sure being backup
        mock_write.assert_called_once_with("testing.taskpaper", task_manager.loaded_taskpaper_data) # make sure being written
        mock_success.assert_called_once_with("Successfully deleted the project 'Project A'.")

if __name__ == "__main__":
    unittest.main()
