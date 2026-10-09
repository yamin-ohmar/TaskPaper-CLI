"""
tests/test_remove_tag.py

Purpose:
    - This does unit testing (automated testing) for 'remove-tag' command
    - To check edge cases from remove_tag() function in src/cli/tag_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_remove_tag.py"
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
from src.managers import tag_manager

class TestRemoveTag(unittest.TestCase):

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_removeTag_tagSymbol_placement(self, mock_show_error, mock_load):
        """[remove-tag] Test 1: tag symbol '@' is placed at wrong location"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.remove_tag("testing.taskpaper", "Project A", "tod@y", "remove-tag") # tag placement wrong
        # test(s)
        mock_show_error.assert_called_once_with("Error: A tag must start with '@' or not contain '@' at all.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_removeTag_empty_tag(self, mock_show_error, mock_load):
        """[remove-tag] Test 2: tag is empty"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.remove_tag("testing.taskpaper", "Project A", " ", "remove-tag") # empty tag name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid tag. The tag name cannot be empty.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_removeTag_withSpace(self, mock_show_error, mock_load):
        """[remove-tag] Test 3: tag name with sapces"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.remove_tag("testing.taskpaper", "Project A", "hi world", "remove-tag") # tag name with sapces
        # test(s)
        mock_show_error.assert_called_once_with("Error: A tag must be a single word without spaces.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.display_project_tasks")
    def test_removeTag_data_not_loaded(self, mock_display, mock_load):
        """[remove-tag] Test 4: not proceeding if data is not loaded"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.remove_tag("testing.taskpaper", "Project A", "@today", "remove-tag")
        # test(s)
        mock_load.assert_called_once()
        mock_display.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_removeTag_noData(self, mock_show_error, mock_load):
        """[remove-tag] Test 5: no data in taskpaper but proceed to check"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.remove_tag("testing.taskpaper", "Project A", "@today", "remove-tag")
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_removeTag_empty_prj_name(self, mock_show_error, mock_load):
        """[remove-tag] Test 6: project name is empty"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.remove_tag("testing.taskpaper", "  ", "@help", "remove-tag") # empty project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_removeTag_no_task(self, mock_show_warning, mock_load):
        """[remove-tag] Test 7: no task in project"""
        tag_manager.task_mng.loaded_taskpaper_data = {"Existing": []}
        tag_manager.remove_tag("testing.taskpaper", "Existing", "@help", "remove-tag")
        # test(s)
        mock_show_warning.assert_called_once_with("There are no tasks under project 'Existing' in file 'testing.taskpaper'.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Existing"], [])

    @patch("src.managers.tag_manager.task_mng.std_input", return_value='hi') # invalid input format
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_removeTag_invalid_input_format(self, mock_load, mock_input):
        """[remove-tag] Test 8: user input invalid format"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            tag_manager.remove_tag("testing.taskpaper", "Project A", "@help", "remove-tag")
            stdout_print = mock_stdout.getvalue()

        # test(s)
        self.assertIn("Invalid input. Please enter a number.", stdout_print)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed

    @patch("src.managers.tag_manager.help_mng.show_error")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='0') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_removeTag_outOfRange_Zero(self, mock_load, mock_input, mock_error):
        """[remove-tag] Test 9: task index out of range (zero)"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.remove_tag("testing.taskpaper", "Project A", "@help", "remove-tag")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 1.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed

    @patch("src.managers.tag_manager.help_mng.show_error")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='3') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_removeTag_outOfRange(self, mock_load, mock_input, mock_error):
        """[remove-tag] Test 10: task index out of range"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.remove_tag("testing.taskpaper", "Project A", "@help", "remove-tag")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 2.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done") # tag not removed

    @patch("src.managers.tag_manager.help_mng.show_warning")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='1')
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_removeTag_not_exist(self, mock_load, mock_input, mock_warning):
        """[remove-tag] Test 11: tag does not exist in the task name"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.remove_tag("testing.taskpaper", "Project A", "@today", "remove-tag")

        # test(s)
        mock_warning.assert_called_once_with("The task 'Old Task @help' does not contain the tag '@today'.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not removed

    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("src.managers.tag_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.tag_manager.undo_mng.save_backup")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='1') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_removeTag_success(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[remove-tag] Test 12: tag removed successfully"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.remove_tag("testing.taskpaper", "Project A", "@help", "remove-tag")

        # test(s)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task") # tag is removed
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done") # not affected
        mock_backup.assert_called_once_with("testing.taskpaper", "remove-tag") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", tag_manager.task_mng.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Tag successfully removed from task: 'Old Task'.") # success message

    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("src.managers.tag_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.tag_manager.undo_mng.save_backup")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='2') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_removeTag_success_noTagSymbol(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[remove-tag] Test 13: tag removed successfully even without '@' symbol in CLI"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.remove_tag("testing.taskpaper", "Project A", "done", "remove-tag")   # without '@' symbol

        # test(s)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # not affected
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2") # tag is added
        mock_backup.assert_called_once_with("testing.taskpaper", "remove-tag") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", tag_manager.task_mng.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Tag successfully removed from task: 'Task 2'.") # success message

    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("src.managers.tag_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.tag_manager.undo_mng.save_backup")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='1') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_removeTag_success_invalid_duedate(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[remove-tag] Test 15: tag removal for incorrect due date formats"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @due(10/01/2025)", "tags": ["@due(10/01/2025)"], "subtasks": []},
                        {"name": "Task 2 @high", "tags": ["@high"], "priority": "high", "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.remove_tag("testing.taskpaper", "Project A", "@due(10/01/2025)", "remove-tag")   # remove invalid due date format

        # test(s)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task") # invalid due date removed
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @high") # not affected
        mock_backup.assert_called_once_with("testing.taskpaper", "remove-tag") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", tag_manager.task_mng.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Tag successfully removed from task: 'Old Task'.") # success message

if __name__ == "__main__":
    unittest.main()
