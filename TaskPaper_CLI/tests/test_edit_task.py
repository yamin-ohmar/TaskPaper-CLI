"""
tests/test_edit_task.py

Purpose:
    - This does unit testing (automated testing) for 'edit-task' command
    - To check edge cases from edit_task() function in src/cli/task_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_edit_task.py"
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

class TestEditTask(unittest.TestCase):

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.display_project_tasks")
    def test_editTask_data_not_loaded(self, mock_display, mock_load):
        """[edit-task] Test 1: not proceeding if data is not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")
        # test(s)
        mock_load.assert_called_once()
        mock_display.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_editTask_noData(self, mock_show_error, mock_load):
        """[edit-task] Test 2: no data in taskpaper but proceed to check"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_editTask_empty_prj_name(self, mock_show_error, mock_load):
        """[edit-task] Test 3: project name is empty"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        task_manager.edit_task("testing.taskpaper", "  ", "edit-task") # empty project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not updated

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_warning")
    def test_editTask_no_task(self, mock_show_warning, mock_load):
        """[edit-task] Test 4: no task in project"""
        task_manager.loaded_taskpaper_data = {"Existing": []}
        task_manager.edit_task("testing.taskpaper", "Existing", "edit-task")
        # test(s)
        mock_show_warning.assert_called_once_with("There are no tasks under project 'Existing' in file 'testing.taskpaper'.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Existing"], []) # no tasks edited in existing project

    @patch("src.managers.task_manager.help_mng.show_error")
    @patch("src.managers.task_manager.std_input", return_value='0 "Updated Task"') # mocking user input
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_editTask_outOfRange_Zero(self, mock_load, mock_input, mock_error):
        """[edit-task] Test 5: task index out of range (zero)"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 1.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not updated

    @patch("src.managers.task_manager.help_mng.show_error")
    @patch("src.managers.task_manager.std_input", return_value='3 "Updated Task"') # mocking user input
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_editTask_outOfRange(self, mock_load, mock_input, mock_error):
        """[edit-task] Test 6: task index out of range"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 2.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not updated
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done") # task not updated

    @patch("src.managers.task_manager.std_input", return_value='1') # invalid input format
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_editTask_invalid_input_format(self, mock_load, mock_input):
        """[edit-task] Test 7: user input invalid format"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")
            stdout_print = mock_stdout.getvalue()

        # test(s)
        self.assertIn("Invalid input. Format should be: <index> \"<updated text>\"", stdout_print)
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not updated

    @patch("src.managers.task_manager.help_mng.show_error")
    @patch("src.managers.task_manager.std_input", return_value='1 " "') # empty updated task
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_editTask_empty_task(self, mock_load, mock_input, mock_error):
        """[edit-task] Test 8: empty task name"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid updated text. The new task name cannot be empty.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not updated

    @patch("src.managers.task_manager.help_mng.show_warning")
    @patch("src.managers.task_manager.std_input", return_value='1 "Old Task @help"') # same task name
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_editTask_same_task(self, mock_load, mock_input, mock_warning):
        """[edit-task] Test 9: same task name"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")

        # test(s)
        mock_warning.assert_called_once_with("Task name remains the same. No changes made.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # task not updated

    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("src.managers.task_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.task_manager.undo_mng.save_backup")
    @patch("src.managers.task_manager.std_input", return_value='1 "Updated Task"') # mocking user input
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_editTask_success(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[edit-task] Test 10: task edited successfully"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            task_manager.edit_task("testing.taskpaper", "Project A", "edit-task")

        # test(s)
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][0]["name"], "Updated Task") # task is updated
        mock_backup.assert_called_once_with("testing.taskpaper", "edit-task") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", task_manager.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Task successfully updated in project 'Project A'.") # success message

if __name__ == "__main__":
    unittest.main()
