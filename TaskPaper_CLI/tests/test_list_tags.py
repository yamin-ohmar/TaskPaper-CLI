"""
tests/test_list_tags.py

Purpose:
    - This does unit testing (automated testing) for 'list-tags' command
    - To check edge cases from list_tags() function in src/cli/tag_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_list_tags.py"
    - [Alternatively] To execute all unit test files inside this venv:
        "python -m unittest discover -s tests"
    - To deactivate this venv after testing:
        "deactivate"

Author: Yamin Ohmar
University: University of Leicester
"""

import sys
import os
import unittest
from unittest.mock import patch

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.managers import task_manager
from src.managers import tag_manager

class TestListTags(unittest.TestCase):

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=False)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_listTags_data_not_loaded(self, mock_error, mock_load):
        """[list-tags] Test 1: not proceeding if data is not loaded"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.list_tags("testing.taskpaper", "Project A")
        # test(s)
        mock_load.assert_called_once()
        mock_error.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_listTags_noData(self, mock_show_error, mock_load):
        """[list-tags] Test 2: no data in taskpaper but proceed to check"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.list_tags("testing.taskpaper", "Project A")
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_listTags_empty_prj_name(self, mock_show_error, mock_load):
        """[list-tags] Test 3: project name is empty"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.list_tags("testing.taskpaper", "  ") # empty project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_listTags_noTag(self, mock_warn, mock_load):
        """[list-tags] Test 4: no tag in project"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task", "tags": [], "subtasks": []}] # no tag
        }
        tag_manager.list_tags("testing.taskpaper", "Project A")
        # test(s)
        mock_warn.assert_called_once_with("No tags found in project 'Project A'.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task")

    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("builtins.print")
    def test_listTags_success(self, mock_print, mock_load, mock_success):
        """[list-tags] Test 5: list tags successfully"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-05-02) @high", "tags": ["@due(2025-05-02)", "@high"], "duedate": "2025-05-02", "priority": "high", "subtasks": []},
                        {"name": "Task 2 @high @today", "tags": ["@high", "@today"], "priority": "high", "subtasks": []}],
            "Project B": [{"name": "Task 1 @today @done", "tags": ["@today", "@done"], "subtasks": []}]
        }
        tag_manager.list_tags("testing.taskpaper", "Project A")
        # test(s): check if it is printed by sorting (A-Z first then a-z)
        mock_print.assert_any_call("1.\t@due(2025-05-02)")
        mock_print.assert_any_call("2.\t@high")
        mock_print.assert_any_call("3.\t@today")
        mock_success.assert_called_once_with("A total of 3 unique tags used in project 'Project A' from file 'testing.taskpaper'.")

if __name__ == "__main__":
    unittest.main()
