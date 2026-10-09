"""
tests/test_add_project.py

Purpose:
    - This does unit testing (automated testing) for 'add-project' command
    - To check edge cases from add_project() function in src/cli/task_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_add_project.py"
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

class TestAddProject(unittest.TestCase):

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.isPrj_exist", return_value=False)
    def test_addPrj_data_not_loaded(self, mock_exist, mock_load):
        """[add-project] Test 1: not proceeding if data is not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.add_project("testing.taskpaper", "New Project", "add-project")
        # making sure load_taskpaper_data() is called once and new project is not added
        mock_load.assert_called_once()
        mock_exist.assert_not_called()  # make sure not proceed
        self.assertNotIn("New Project", task_manager.loaded_taskpaper_data)

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_addPrj_empty_name(self, mock_show_error, mock_load):
        """[add-project] Test 2: project name is empty"""
        task_manager.loaded_taskpaper_data = {"Existing": []}
        task_manager.add_project("testing.taskpaper", "   ", "add-project") # empty project name
        # making sure show_error func was called exactly once with below error message as argument 
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_addPrj_already_exists(self, mock_show_warning, mock_load):
        """[add-project] Test 3: project name is duplicated"""
        task_manager.loaded_taskpaper_data = {"Project A": []}
        task_manager.add_project("testing.taskpaper", "Project A", "add-project") # duplicate project name
        # making sure show_warning func was called exactly once with below warning message as argument 
        mock_show_warning.assert_called_once_with("Project 'Project A' already exists.")

    # using mock objects for functions that is used for this testing
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("src.managers.task_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.task_manager.undo_mng.save_backup")
    def test_addPrj_success(self, mock_backup, mock_write, mock_success, mock_load):
        """[add-project] Test 4: new project added successfully"""
        task_manager.loaded_taskpaper_data = {"Existing": []}

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            task_manager.add_project("testing.taskpaper", "New Project", "add-project")
            stdout_print = mock_stdout.getvalue()
        
        # making sure the project was added to memory
        self.assertIn("New Project", task_manager.loaded_taskpaper_data)
        self.assertEqual(task_manager.loaded_taskpaper_data["New Project"], []) # no tasks
        self.assertIn("Adding project 'New Project' to file 'testing.taskpaper'...", stdout_print)

        # making sure helper functions (mocked functions) were called with below arguments
        mock_backup.assert_called_once_with("testing.taskpaper", "add-project")
        mock_write.assert_called_once_with("testing.taskpaper", task_manager.loaded_taskpaper_data)
        mock_success.assert_called_once_with("Added project 'New Project' successfully.")

    # using mock objects for functions that is used for this testing
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("src.managers.task_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.task_manager.undo_mng.save_backup")
    def test_addPrj_noData_success(self, mock_backup, mock_write, mock_success, mock_load):
        """[add-project] Test 5: new project added successfully when no data in file"""
        task_manager.loaded_taskpaper_data = {} # no data in file

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            task_manager.add_project("testing.taskpaper", "Project A", "add-project")
            stdout_print = mock_stdout.getvalue()
        
        # making sure the project was added to memory
        self.assertIn("Project A", task_manager.loaded_taskpaper_data)
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"], []) # no tasks
        self.assertIn("Adding project 'Project A' to file 'testing.taskpaper'...", stdout_print)

        # making sure helper functions (mocked functions) were called with below arguments
        mock_backup.assert_called_once_with("testing.taskpaper", "add-project")
        mock_write.assert_called_once_with("testing.taskpaper", task_manager.loaded_taskpaper_data)
        mock_success.assert_called_once_with("Added project 'Project A' successfully.")

if __name__ == "__main__":
    unittest.main()
