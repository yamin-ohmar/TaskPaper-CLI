"""
tests/test_add_task.py

Purpose:
    - This does unit testing (automated testing) for 'add-task' command
    - To check edge cases from add_task() function in src/cli/task_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_add_task.py"
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

class TestAddTask(unittest.TestCase):

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.isPrj_exist", return_value=False)
    def test_addTask_data_not_loaded(self, mock_exist, mock_load):
        """[add-task] Test 1: not proceeding if data is not loaded"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.add_task("testing.taskpaper", "Project A", "Task 1", "add-task")
        # test(s)
        mock_load.assert_called_once()
        mock_exist.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_addTask_noData(self, mock_show_error, mock_load):
        """[add-task] Test 2: no data in taskpaper but proceed to check"""
        task_manager.loaded_taskpaper_data = {}
        task_manager.add_task("testing.taskpaper", "Project A", "Task 1", "add-task")
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", task_manager.loaded_taskpaper_data)

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_addTask_empty_prj_name(self, mock_show_error, mock_load):
        """[add-task] Test 3: project name is empty"""
        task_manager.loaded_taskpaper_data = {"Existing": []}
        task_manager.add_task("testing.taskpaper", "", "Task 1", "add-task") # empty project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name (or) task name. The name(s) cannot be empty.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Existing"], []) # no tasks added to existing

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_error")
    def test_addTask_empty_task_name(self, mock_show_error, mock_load):
        """[add-task] Test 4: task name is empty"""
        task_manager.loaded_taskpaper_data = {"Existing": []}
        task_manager.add_task("testing.taskpaper", "Existing", "  ", "add-task") # empty task name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name (or) task name. The name(s) cannot be empty.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Existing"], []) # no tasks added to existing

    @patch("src.managers.task_manager.help_mng.show_error")
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_addTask_prj_not_exist(self, mock_load, mock_show_error):
        """[add-task] Test 5: project does not exist"""
        task_manager.loaded_taskpaper_data = {"Project A": []}
        task_manager.add_task("testing.taskpaper", "Nonexistent", "Task 1", "add-task")
        # test(s)
        mock_show_error.assert_called_once_with("Error: Project 'Nonexistent' does not exist in file 'testing.taskpaper'.")
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"], []) # no tasks added to existing

    @patch("src.managers.task_manager.help_mng.show_warning")
    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    def test_addTask_task_exists(self, mock_load, mock_show_warning):
        """[add-task] Test 6: task name is duplicated"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Task A @today", "tags": ["@today"], "subtasks": []},
                {"name": "Task B", "tags": [], "subtasks": []}
            ]
        }
        task_manager.add_task("testing.taskpaper", "Project A", "Task A @today", "add-task")
        # test(s)
        mock_show_warning.assert_called_once_with("Task 'Task A @today' already exists in project 'Project A'.")
        self.assertIn("Task A @today", task_manager.loaded_taskpaper_data["Project A"][0]["name"])

    @patch("src.managers.task_manager.load_taskpaper_data", return_value=True)
    @patch("src.managers.task_manager.help_mng.show_success")
    @patch("src.managers.task_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.task_manager.undo_mng.save_backup")
    def test_addTask_success(self, mock_backup, mock_write, mock_success, mock_load):
        """[add-task] Test 7: new task added successfully"""
        task_manager.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Task A @done", "tags": ["@done"], "subtasks": []},
                {"name": "Task B", "tags": [], "subtasks": []}
            ]
        }

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            task_manager.add_task("testing.taskpaper", "Project A", "Task C @today", "add-task")
            stdout_print = mock_stdout.getvalue()
        
        # making sure the task was added to memory
        self.assertIn("Task C @today", task_manager.loaded_taskpaper_data["Project A"][2]["name"])
        self.assertEqual(task_manager.loaded_taskpaper_data["Project A"][2]["subtasks"], []) # no subtasks
        self.assertIn("Adding task 'Task C @today' to project 'Project A' in file 'testing.taskpaper'...", stdout_print)

        # making sure helper functions (mocked functions) were called with below arguments
        mock_backup.assert_called_once_with("testing.taskpaper", "add-task")
        mock_write.assert_called_once_with("testing.taskpaper", task_manager.loaded_taskpaper_data)
        mock_success.assert_called_once_with("Added task 'Task C @today' successfully.")

if __name__ == "__main__":
    unittest.main()
