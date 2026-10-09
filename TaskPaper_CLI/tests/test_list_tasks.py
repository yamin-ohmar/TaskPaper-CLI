"""
tests/test_list_tasks.py

Purpose:
    - This does unit testing (automated testing) for 'list-tasks' command
    - To check edge cases from list_tasks() function in src/cli/task_manager.py
    and src/cli/tag_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_list_tasks.py"
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
from tabulate import tabulate
from termcolor import colored

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.managers import task_manager
from src.managers import tag_manager

class TestListTasks(unittest.TestCase):

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.display_project_tasks")
    def test_listTasks_woTag_data_not_loaded(self, mock_display, mock_load):
        """[list-tasks w/o tag] Test 1: not proceeding if data is not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.list_tasks("testing.taskpaper", "Project A")
        # test(s)
        mock_load.assert_called_once()
        mock_display.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.display_project_tasks", return_value=None)
    def test_listTasks_woTag_noData(self, mock_display, mock_load):
        """[list-tasks w/o tag] Test 2: no data in taskpaper but proceed to call display function"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.list_tasks("testing.taskpaper", "Project A")
        # test(s)
        mock_load.assert_called_once()
        mock_display.assert_called_once_with("testing.taskpaper", "Project A")
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_listTasks_woTag_prjNotExist(self, mock_show_error, mock_load):
        """[list-tasks w/o tag] Test 3: project does not exist"""
        task_manager.loaded_taskpaper_data = {"Existing": []}
        task_manager.list_tasks("testing.taskpaper", "Project A")
        # test(s)
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)
        self.assertIn("Existing", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_listTasks_woTag_emptyPrj(self, mock_show_error, mock_load):
        """[list-tasks w/o tag] Test 4: project name is empty"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        task_manager.list_tasks("testing.taskpaper", "  ") # empty project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_listTasks_no_task(self, mock_show_warning, mock_load):
        """[list-tasks w/o tag] Test 5: no task in project"""
        task_manager.loaded_taskpaper_data = {"Existing": []}
        task_manager.list_tasks("testing.taskpaper", "Existing")
        # test(s)
        mock_show_warning.assert_called_once_with("There are no tasks under project 'Existing' in file 'testing.taskpaper'.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Existing"], []) # no tasks

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("builtins.print")
    def test_listTasks_success(self, mock_print, mock_success, mock_load):
        """[list-tasks w/o tag] Test 6: list (print) tasks successfully"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}],
            "Project B": [{"name": "New Task @due(2025-03-30)", "tags": ["@due(2025-03-30)"], "duedate": "2025-03-30", "priority": None, "subtasks": []}]
        }
        task_manager.list_tasks("testing.taskpaper", "Project A")
        # test(s)
        mock_print.assert_any_call("Tasks in project 'Project A':")
        mock_print.assert_any_call("1. Old Task @help") # check if task 1 printed
        mock_print.assert_any_call("2. Task 2 @done") # check if task 2 printed
        mock_success.assert_called_once_with("A total of 2 task(s) listed for project 'Project A' from file 'testing.taskpaper'.")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=False)
    @patch("src.managers.tag_manager.validate_tag")
    def test_listTasks_wTag_data_not_loaded(self, mock_validate, mock_load):
        """[list-tasks with tag] Test 7: not proceeding if data is not loaded"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.list_tasks("testing.taskpaper", None, "@today")
        # test(s)
        mock_load.assert_called_once()
        mock_validate.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.validate_tag")
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_listTasks_wTag_noData(self, mock_warning, mock_validate, mock_load):
        """[list-tasks with tag] Test 8: no data in taskpaper but proceed to call validate function"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.list_tasks("testing.taskpaper", None, "@today")
        # test(s)
        mock_load.assert_called_once()
        mock_validate.assert_called_once_with("@today", check_duedate=True)  # make sure not proceed
        mock_warning.assert_called_once_with("No matching tasks found.")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_listTasks_wTag_emptyPrj(self, mock_error, mock_load):
        """[list-tasks with tag] Test 9: empty project name"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @today", "tags": ["@today"], "duedate": None, "priority": None, "subtasks": []}]
        }
        tag_manager.list_tasks("testing.taskpaper", "  ", "@today") # empty project name
        # test(s)
        mock_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_listTasks_wTag_prjNotExist(self, mock_error, mock_load):
        """[list-tasks with tag] Test 10: project does not exist"""
        tag_manager.task_mng.loaded_taskpaper_data = {"Existing": []}
        tag_manager.list_tasks("testing.taskpaper", "Project A", "@today")
        # test(s)
        mock_load.assert_called_once()
        mock_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.print_colorLegend")
    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("builtins.print")
    def test_listTasks_wTag_success_inPrj(self, mock_print, mock_success, mock_legend, mock_load):
        """[list-tasks with tag] Test 11: successfully print matching tasks under the specific project"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(2025-03-30)", "tags": ["@due(2025-03-30)"], "duedate": "2025-03-30", "priority": None, "subtasks": []}],
            "Project B": [{"name": "New Task @due(2025-02-02) @done", "tags": ["@due(2025-02-02)", "@done"], "duedate": "2025-02-02", "priority": None, "subtasks": []},
                          {"name": "Task @low @due(2025-06-03)", "tags": ["@low", "@due(2025-06-03)"], "duedate": "2025-06-03", "priority": "low", "subtasks": []},
                          {"name": "Old Task @high @due(2025-03-03)", "tags": ["@high", "@due(2025-03-03)"], "duedate": "2025-03-03", "priority": "high", "subtasks": []}]
        }
        tag_manager.list_tasks("testing.taskpaper", "Project B", "@due") # check project B only for all tasks with due date
        # expected printing result (sorted by priority level and colored by due date)
        expected_print = tabulate(
            [[1, "Project B", colored("Old Task @high @due(2025-03-03)", "red"), "high"],
            [2, "Project B", "Task @low @due(2025-06-03)", "low"],
            [3, "Project B", colored("New Task @due(2025-02-02) @done", "green"), ""]],
            headers=["No.", "Project", "Task Name", "Priority"],
            tablefmt="rst"
        ) + "\n"
        # test(s) check if it is sorted by priority level
        mock_legend.assert_called_once()
        mock_print.assert_any_call(expected_print)
        mock_success.assert_called_once_with("A total of 3 task(s) listed from file 'testing.taskpaper'.")

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.print_colorLegend")
    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("builtins.print")
    def test_listTasks_wTag_success_inFile(self, mock_print, mock_success, mock_legend, mock_load):
        """[list-tasks with tag] Test 12: successfully print matching tasks from the whole file"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @done @priority(medium)", "tags": ["@done", "@priority(medium)"], "duedate": None, "priority": "medium", "subtasks": []}],
            "Project B": [{"name": "New Task @due(2025-02-02) @done", "tags": ["@due(2025-02-02)", "@done"], "duedate": "2025-02-02", "priority": None, "subtasks": []},
                          {"name": "Task @low @due(2025-06-03)", "tags": ["@low", "@due(2025-06-03)"], "duedate": "2025-06-03", "priority": "low", "subtasks": []},
                          {"name": "Old Task @high @due(2025-03-03)", "tags": ["@high", "@due(2025-03-03)"], "duedate": "2025-03-03", "priority": "high", "subtasks": []}]
        }
        tag_manager.list_tasks("testing.taskpaper", None, "@priority") # check the whole file for all tasks with priority
        # expected printing result (sorted by priority level and colored by due date)
        expected_print = tabulate(
            [[1, "Project B", colored("Old Task @high @due(2025-03-03)", "red"), "high"],
            [2, "Project A", colored("Old Task @done @priority(medium)", "green"), "medium"],
            [3, "Project B", "Task @low @due(2025-06-03)", "low"]],
            headers=["No.", "Project", "Task Name", "Priority"],
            tablefmt="rst"
        ) + "\n"
        # test(s) check if it is sorted by priority level
        mock_legend.assert_called_once()
        mock_print.assert_any_call(expected_print)
        mock_success.assert_called_once_with("A total of 3 task(s) listed from file 'testing.taskpaper'.")

if __name__ == "__main__":
    unittest.main()
