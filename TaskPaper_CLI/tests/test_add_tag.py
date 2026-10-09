"""
tests/test_add_tag.py

Purpose:
    - This does unit testing (automated testing) for 'add-tag' command
    - To check edge cases from add_tag() function in src/cli/tag_manager.py

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_add_tag.py"
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

class TestAddTag(unittest.TestCase):

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_addTag_tagSymbol_placement(self, mock_show_error, mock_load):
        """[add-tag] Test 1: tag symbol '@' is placed at wrong location"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.add_tag("testing.taskpaper", "Project A", "tod@y", "add-tag") # tag placement wrong
        # test(s)
        mock_show_error.assert_called_once_with("Error: A tag must start with '@' or not contain '@' at all.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_addTag_empty_tag(self, mock_show_error, mock_load):
        """[add-tag] Test 2: tag is empty"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.add_tag("testing.taskpaper", "Project A", " ", "add-tag") # empty tag name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid tag. The tag name cannot be empty.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_addTag_withSpace(self, mock_show_error, mock_load):
        """[add-tag] Test 3: tag name with sapces"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.add_tag("testing.taskpaper", "Project A", "hi world", "add-tag") # tag name with sapces
        # test(s)
        mock_show_error.assert_called_once_with("Error: A tag must be a single word without spaces.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_addTag_invalid_duedate(self, mock_show_error, mock_load):
        """[add-tag] Test 4: invalid due date tag"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.add_tag("testing.taskpaper", "Project A", "@due(01-10-2025)", "add-tag") # due date invalid format
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid due date format. Please use '@due(YYYY-MM-DD)'.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=False)
    @patch("src.managers.task_manager.display_project_tasks")
    def test_addTag_data_not_loaded(self, mock_display, mock_load):
        """[add-tag] Test 5: not proceeding if data is not loaded"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.add_tag("testing.taskpaper", "Project A", "@today", "add-tag")
        # test(s)
        mock_load.assert_called_once()
        mock_display.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_addTag_noData(self, mock_show_error, mock_load):
        """[add-tag] Test 6: no data in taskpaper but proceed to check"""
        tag_manager.task_mng.loaded_taskpaper_data = {}
        tag_manager.add_tag("testing.taskpaper", "Project A", "@today", "add-tag")
        # test(s)
        mock_load.assert_called_once()
        mock_show_error.assert_called_once_with("Error: Project 'Project A' does not exist in file 'testing.taskpaper'.")
        self.assertNotIn("Project A", tag_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_error")
    def test_addTag_empty_prj_name(self, mock_show_error, mock_load):
        """[add-tag] Test 7: project name is empty"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }
        tag_manager.add_tag("testing.taskpaper", "  ", "@today", "add-tag") # empty project name
        # test(s)
        mock_show_error.assert_called_once_with("Error: Invalid project name. The name cannot be empty.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added

    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.tag_manager.help_mng.show_warning")
    def test_addTag_no_task(self, mock_show_warning, mock_load):
        """[add-tag] Test 8: no task in project"""
        tag_manager.task_mng.loaded_taskpaper_data = {"Existing": []}
        tag_manager.add_tag("testing.taskpaper", "Existing", "@today", "add-tag")
        # test(s)
        mock_show_warning.assert_called_once_with("There are no tasks under project 'Existing' in file 'testing.taskpaper'.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Existing"], []) # no tag added

    @patch("src.managers.tag_manager.task_mng.std_input", return_value='"hi world"') # invalid input format
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_addTag_invalid_input_format(self, mock_load, mock_input):
        """[add-tag] Test 9: user input invalid format"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        # redirecting stdout to capture print() output
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            tag_manager.add_tag("testing.taskpaper", "Project A", "@today", "add-tag")
            stdout_print = mock_stdout.getvalue()

        # test(s)
        self.assertIn("Invalid input. Please enter a number.", stdout_print)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added

    @patch("src.managers.tag_manager.help_mng.show_error")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='0') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_addTag_outOfRange_Zero(self, mock_load, mock_input, mock_error):
        """[add-tag] Test 10: task index out of range (zero)"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.add_tag("testing.taskpaper", "Project A", "@today", "add-tag")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 1.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added

    @patch("src.managers.tag_manager.help_mng.show_error")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='3') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_addTag_outOfRange(self, mock_load, mock_input, mock_error):
        """[add-tag] Test 11: task index out of range"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.add_tag("testing.taskpaper", "Project A", "@today", "add-tag")

        # test(s)
        mock_error.assert_called_once_with("Error: Invalid index. Must be from 1 to 2.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done") # tag not added

    @patch("src.managers.tag_manager.help_mng.show_warning")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='1')
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_addTag_duplicate_tag(self, mock_load, mock_input, mock_warning):
        """[add-tag] Test 12: duplicated tag in task"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.add_tag("testing.taskpaper", "Project A", "@help", "add-tag")

        # test(s)
        mock_warning.assert_called_once_with("Task 'Old Task @help' already has the tag '@help'.")
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # tag not added twice

    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("src.managers.tag_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.tag_manager.undo_mng.save_backup")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='1') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_addTag_success(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[add-tag] Test 13: tag added successfully"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.add_tag("testing.taskpaper", "Project A", "@today", "add-tag")

        # test(s)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help @today") # tag is added
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done") # not affected
        mock_backup.assert_called_once_with("testing.taskpaper", "add-tag") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", tag_manager.task_mng.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Tag successfully added to task: 'Old Task @help @today'.") # success message

    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("src.managers.tag_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.tag_manager.undo_mng.save_backup")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='2') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_addTag_success_noTagSymbol(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[add-tag] Test 14: tag added successfully even without '@' symbol in CLI"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @done", "tags": ["@done"], "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.add_tag("testing.taskpaper", "Project A", "today", "add-tag")   # without '@' symbol

        # test(s)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # not affected
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @done @today") # tag is added
        mock_backup.assert_called_once_with("testing.taskpaper", "add-tag") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", tag_manager.task_mng.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Tag successfully added to task: 'Task 2 @done @today'.") # success message

    @patch("src.managers.tag_manager.help_mng.show_success")
    @patch("src.managers.tag_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.tag_manager.undo_mng.save_backup")
    @patch("src.managers.tag_manager.task_mng.std_input", return_value='2') # mocking user input
    @patch("src.managers.tag_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_addTag_duedate_success(self, mock_load, mock_input, mock_backup, mock_write, mock_success):
        """[add-tag] Test 15: tag added successfully with correct due date format"""
        tag_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [{"name": "Old Task @help", "tags": ["@help"], "subtasks": []},
                        {"name": "Task 2 @high", "tags": ["@high"], "priority": "high", "subtasks": []}]
        }

        with patch("sys.stdout"):  # suppress printing
            tag_manager.add_tag("testing.taskpaper", "Project A", "@due(2025-05-02)", "add-tag")   # valid due date format

        # test(s)
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"], "Old Task @help") # not affected
        self.assertEqual(tag_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"], "Task 2 @high @due(2025-05-02)") # tag is added
        mock_backup.assert_called_once_with("testing.taskpaper", "add-tag") # being backup
        mock_write.assert_called_once_with("testing.taskpaper", tag_manager.task_mng.loaded_taskpaper_data) # writing is called
        mock_success.assert_called_once_with("Tag successfully added to task: 'Task 2 @high @due(2025-05-02)'.") # success message

if __name__ == "__main__":
    unittest.main()
