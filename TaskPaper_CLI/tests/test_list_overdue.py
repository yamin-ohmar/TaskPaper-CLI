"""
tests/test_list_overdue.py

Purpose:
    - This does unit testing (automated testing) for 'list-overdue' command
    - To check edge cases from list_overdue() function in src/cli/tag_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_list_overdue.py"
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
from tabulate import tabulate

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.managers import task_manager
from src.managers import tag_manager

class TestListTags(unittest.TestCase):

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=False)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_listOverdue_data_not_loaded(self, mock_warn, mock_load):
        """[list-overdue] Test 1: not proceeding if data is not loaded"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.list_overdue("testing.taskpaper")
        # test(s)
        mock_load.assert_called_once()
        mock_warn.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_listOverdue_noData(self, mock_warn, mock_load):
        """[list-overdue] Test 2: no data in taskpaper but proceed to check"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.list_overdue("testing.taskpaper")
        # test(s)
        mock_load.assert_called_once()
        mock_warn.assert_called_once_with("No overdue tasks found.")  # make sure proceeded
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_listOverdue_empty_prject(self, mock_error, mock_load):
        """[list-overdue] Test 3: empty project name"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-03-30)", "tags": ["@due(2025-03-30)"], "duedate": "2025-03-30", "priority": None, "subtasks": []}]
        }
        tag_manager.list_overdue("testing.taskpaper", "  ")   # empty project name
        # test(s)
        mock_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @due(2025-03-30)")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_listOverdue_noOverdueTask_inPrj(self, mock_warn, mock_load):
        """[list-overdue] Test 4: no overdue task in the project"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-06-30)", "tags": ["@due(2025-06-30)"], "duedate": "2025-06-30", "priority": None, "subtasks": []}],
            "Project B": [{"name": "New Task @due(2025-03-30)", "tags": ["@due(2025-03-30)"], "duedate": "2025-03-30", "priority": None, "subtasks": []}]
        }
        tag_manager.list_overdue("testing.taskpaper", "Project A") # check project A only
        # test(s)
        mock_warn.assert_called_once_with("No overdue tasks found.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @due(2025-06-30)")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_listOverdue_noOverdueTask_inPrj(self, mock_warn, mock_load):
        """[list-overdue] Test 4: no overdue task in the project"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-06-30)", "tags": ["@due(2025-06-30)"], "duedate": "2025-06-30", "priority": None, "subtasks": []}],
            "Project B": [{"name": "New Task @due(2025-03-30)", "tags": ["@due(2025-03-30)"], "duedate": "2025-03-30", "priority": None, "subtasks": []}]
        }
        tag_manager.list_overdue("testing.taskpaper", "Project A") # check project A only
        # test(s)
        mock_warn.assert_called_once_with("No overdue tasks found.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @due(2025-06-30)")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_listOverdue_noOverdueTask_inFile(self, mock_warn, mock_load):
        """[list-overdue] Test 5: no overdue task in the file"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-06-30)", "tags": ["@due(2025-06-30)"], "duedate": "2025-06-30", "priority": None, "subtasks": []}],
            "Project B": [{"name": "New Task @due(2025-05-30)", "tags": ["@due(2025-05-30)"], "duedate": "2025-05-30", "priority": None, "subtasks": []}]
        }
        tag_manager.list_overdue("testing.taskpaper") # check whole file
        # test(s)
        mock_warn.assert_called_once_with("No overdue tasks found.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @due(2025-06-30)")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project B"][0]["name"], "New Task @due(2025-05-30)")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("builtins.print")
    def test_listOverdue_success_inPrj(self, mock_print, mock_success, mock_load):
        """[list-overdue] Test 6: successfully print overdue task in the project"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-03-30)", "tags": ["@due(2025-03-30)"], "duedate": "2025-03-30", "priority": None, "subtasks": []}],
            "Project B": [{"name": "New Task @due(2025-02-02) @medium", "tags": ["@due(2025-02-02)", "@medium"], "duedate": "2025-02-02", "priority": "medium", "subtasks": []},
                          {"name": "Task @low @due(2025-06-03)", "tags": ["@low", "@due(2025-06-03)"], "duedate": "2025-06-03", "priority": "low", "subtasks": []},
                          {"name": "Old Task @high @due(2025-03-03)", "tags": ["@high", "@due(2025-03-03)"], "duedate": "2025-03-03", "priority": "high", "subtasks": []}]
        }
        tag_manager.list_overdue("testing.taskpaper", "Project B") # check project B only
        # expected printing result
        expected_print = "\n" + tabulate(
            [[1, "Project B", "Old Task @high @due(2025-03-03)", "high"],
            [2, "Project B", "New Task @due(2025-02-02) @medium", "medium"]],
            headers=["No.", "Project", "Overdue Task(s)", "Priority"],
            tablefmt="rst"
        ) + "\n"
        # test(s) check if it is sorted by priority level
        mock_print.assert_any_call(expected_print)
        mock_success.assert_called_once_with("A total of 2 overdue task(s) listed from file 'testing.taskpaper'.")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("builtins.print")
    def test_listOverdue_success_inFile(self, mock_print, mock_success, mock_load):
        """[list-overdue] Test 7: successfully print overdue task in file"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-06-30)", "tags": ["@due(2025-06-30)"], "duedate": "2025-06-30", "priority": None, "subtasks": []},
                          {"name": "New Task @due(2025-03-30)", "tags": ["@due(2025-03-30)"], "duedate": "2025-03-30", "priority": None, "subtasks": []}],
            "Project B": [{"name": "Task 1 @due(2025-02-02) @medium @done", "tags": ["@due(2025-02-02)", "@medium", "@done"], "duedate": "2025-02-02", "priority": "medium", "subtasks": []},
                          {"name": "Task @low @due(2025-06-03)", "tags": ["@low", "@due(2025-06-03)"], "duedate": "2025-06-03", "priority": "low", "subtasks": []},
                          {"name": "Old Task @high @due(2025-03-03)", "tags": ["@high", "@due(2025-03-03)"], "duedate": "2025-03-03", "priority": "high", "subtasks": []}]
        }
        tag_manager.list_overdue("testing.taskpaper") # check in whole file
        # expected printing result
        expected_print = "\n" + tabulate(
            [[1, "Project B", "Old Task @high @due(2025-03-03)", "high"],
            [2, "Project A", "New Task @due(2025-03-30)", ""]],
            headers=["No.", "Project", "Overdue Task(s)", "Priority"],
            tablefmt="rst"
        ) + "\n"
        # test(s) check if it is sorted by priority level
        mock_print.assert_any_call(expected_print)
        mock_success.assert_called_once_with("A total of 2 overdue task(s) listed from file 'testing.taskpaper'.")

if __name__ == "__main__":
    unittest.main()
