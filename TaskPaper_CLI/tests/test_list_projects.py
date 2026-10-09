"""
tests/test_list_projects.py

Purpose:
    - This does unit testing (automated testing) for 'list-projects' command
    - To check edge cases from get_all_projects() function in src/cli/task_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_list_projects.py"
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

class TestListProjects(unittest.TestCase):

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_listPrj_data_not_loaded(self, mock_warning, mock_load):
        """[list-projects] Test 1: data not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.get_all_projects("testing.taskpaper")
        # test(s)
        mock_load.assert_called_once()
        mock_warning.assert_not_called()

    # using mock objects
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_listPrj_no_project(self, mock_warning, mock_load):
        """[list-projects] Test 2: no project in file"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.get_all_projects("testing.taskpaper")
        # test(s)
        mock_warning.assert_called_once_with("There are no project in file 'testing.taskpaper'.")

    # using mock objects (including printing)
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("builtins.print")
    def test_listPrj_success(self, mock_print, mock_success, mock_load):
        """[list-projects] Test 3: list (print) projects successfully"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [],
            "Project B": []
        }
        task_manager.get_all_projects("testing.taskpaper")
        # test(s)
        mock_print.assert_any_call("1.\tProject A") # check if it is printed
        mock_print.assert_any_call("2.\tProject B") # check if it is printed
        mock_success.assert_called_once_with("A total of 2 project(s) listed from file 'testing.taskpaper'.")

if __name__ == "__main__":
    unittest.main()
