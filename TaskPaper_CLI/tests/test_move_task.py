"""
tests/test_move_task.py

Purpose:
    - This does unit testing (automated testing) for 'move-task' command
    - To check edge cases from move_task() function in src/cli/task_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_move_task.py"
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

class TestMoveTask(unittest.TestCase):

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.display_project_tasks")
    def test_moveTask_data_not_loaded(self, mock_display, mock_load):
        """[move-task] Test 1: not proceeding if data is not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task")
        # test(s)
        mock_load.assert_called_once()
        mock_display.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_moveTask_noData_destPrj_notexist(self, mock_show_error, mock_load):
        """[move-task] Test 2: no data in taskpaper but proceed to check destination project first"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task") # move from project A to B
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project B' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_moveTask_srcPrj_notexist(self, mock_show_error, mock_load):
        """[move-task] Test 3: source project does not exist"""
        task_manager.loaded_taskpaper_data = {
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }
        task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task") # move from project A to B
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_moveTask_empty_destPrj_name(self, mock_show_error, mock_load):
        """[move-task] Test 4: destination project name is empty"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }
        task_manager.move_task("testing.taskpaper", "Project A", "  ", "move-task") # empty destination project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][0]["name"], "New Task @today") # task not moved

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_moveTask_empty_srcPrj_name(self, mock_show_error, mock_load):
        """[move-task] Test 5: destination project name is empty"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }
        task_manager.move_task("testing.taskpaper", "", "Project B", "move-task") # empty source project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][0]["name"], "New Task @today") # task not moved

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_moveTask_same_project(self, mock_warning, mock_load):
        """[move-task] Test 6: destination project and source project are the same"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }
        task_manager.move_task("testing.taskpaper", "Project B", "Project B", "move-task") # same project names
        # test(s)
        mock_warning.assert_called_once_with("Source project name and destination project name are the same. No changes made.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][0]["name"], "New Task @today") # task not moved

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_moveTask_no_task(self, mock_show_warning, mock_load):
        """[move-task] Test 7: no task in source project"""
        task_manager.loaded_taskpaper_data = {"Existing": [], "Next": []}
        task_manager.move_task("testing.taskpaper", "Existing", "Next", "move-task")
        # test(s)
        mock_show_warning.assert_called_once_with("There are no tasks under project 'Existing' in file 'testing.taskpaper'.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Existing"], []) # no tasks in source project
        self.assertEqual(task_manager.loaded_taskpaper_data["Next"], []) # no tasks in destination project

    @patch("src.managers.task_manager.help_mng.show_error")
    @patch("src.managers.task_manager.std_input", return_value='0') # mocking user input
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_moveTask_outOfRange_Zero(self, mock_load, mock_input, mock_error):
        """[move-task] Test 8: task index out of range (zero)"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 1.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][0]["name"], "New Task @today") # task not moved

    @patch("src.managers.task_manager.help_mng.show_error")
    @patch("src.managers.task_manager.std_input", return_value='3') # mocking user input
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_moveTask_outOfRange(self, mock_load, mock_input, mock_error):
        """[move-task] Test 9: task index out of range"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 2.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][0]["name"], "New Task @today") # task not moved

    @patch("src.managers.task_manager.std_input", return_value='abc') # invalid input format
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_moveTask_invalid_input_format(self, mock_load, mock_input):
        """[move-task] Test 10: user input invalid format"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task")
            stdout_print = mock_stdout.getvalue()

        # test(s)
        self.assertIn("Invalid input. Please enter a number.", stdout_print)
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][0]["name"], "New Task @today") # task not moved

    @patch("src.managers.task_manager.help_mng.show_warning")
    @patch("src.managers.task_manager.undo_mng.save_backup")
    @patch("src.managers.task_manager.std_input", side_effect=['1', 'n']) # for sequence of user inputs
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_moveTask_cancel(self, mock_load, mock_input, mock_backup, mock_warning):
        """[move-task] Test 11: task move being cancelled"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task")

        # test(s)
        mock_warning.assert_called_once_with("Task moving cancelled.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not deleted
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done") # task not moved
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][0]["name"], "New Task @today") # task not moved
        mock_backup.assert_not_called() # not proceed with backup

    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("src.managers.task_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.task_manager.undo_mng.save_backup")
    @patch("src.managers.task_manager.std_input", side_effect=['1', 'y']) # delete 1st task then 'y' for confirmation
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_moveTask_success(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[move-task] Test 12: task moved successfully"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}],
            "Project B": [{"name": "New Task @today", "tags": ["@today"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.move_task("testing.taskpaper", "Project A", "Project B", "move-task")

        # test(s)
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Task 2 @done") # Task 2 becomes 1st task
        self.assertEqual(task_manager.loaded_taskpaper_data["Project B"][1]["name"], "Old Task @help") # Task moved from Project B
        mock_backup.assert_called_once_with("testing.taskpaper", "move-task") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", task_manager.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Task successfully moved from project 'Project A' to project 'Project B'.") # success message

if __name__ == "__main__":
    unittest.main()
