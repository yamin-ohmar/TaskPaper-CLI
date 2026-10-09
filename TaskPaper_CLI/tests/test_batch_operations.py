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
from unittest.mock import call, patch

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.managers import task_manager
from src.managers import tag_manager
from src.managers import batch_manager

class TestBatchOperations(unittest.TestCase):

    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=False)
    @patch("src.managers.batch_manager.tag_mng.validate_tag")
    def test_batch_data_not_loaded(self, mock_validate, mock_load):
        """[batch] Test 1: not proceeding if data is not loaded"""
        batch_manager.task_mng.loaded_taskpaper_data = {}
        batch_manager.batch_operation("testing.taskpaper", "@today", "mark-done", "batch")
        # test(s)
        mock_load.assert_called_once()
        mock_validate.assert_not_called()  # make sure not proceed
        self.assertNotIn("Project A", batch_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.batch_manager.tag_mng.validate_tag")
    @patch("src.managers.batch_manager.help_mng.show_warning")
    def test_batch_noData_markDone(self, mock_warn, mock_validate, mock_load):
        """[batch mark-done] Test 2: no data, but proceed to validate tag"""
        batch_manager.task_mng.loaded_taskpaper_data = {}
        batch_manager.batch_operation("testing.taskpaper", "@today", "mark-done", "batch")
        # test(s)
        mock_load.assert_called_once()
        mock_validate.assert_called_once_with("@today", check_duedate=True)
        self.assertNotIn("Project A", batch_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.batch_manager.tag_mng.validate_tag")
    @patch("src.managers.batch_manager.help_mng.show_warning")
    def test_batch_noData_replaceTag(self, mock_warn, mock_validate, mock_load):
        """[batch replace-tag] Test 3: no data, but proceed to validate 2 tags"""
        batch_manager.task_mng.loaded_taskpaper_data = {}
        batch_manager.batch_operation("testing.taskpaper", "@today", "replace-tag", "batch", "@tomorrow")
        # test(s)
        mock_load.assert_called_once()
        expected_calls = [
            call("@today", check_duedate=True),
            call("@tomorrow", check_duedate=True)
        ] # checking if it's called twice with 2 different tags
        self.assertEqual(mock_validate.call_args_list[:2], expected_calls)
        self.assertNotIn("Project A", batch_manager.task_mng.loaded_taskpaper_data)

    @patch("src.managers.batch_manager.mark_done")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.batch_manager.tag_mng.validate_tag", return_value = "@today")
    def test_batch_call_markDone(self, mock_validate, mock_load, mock_mark_done):
        """[batch mark-done] Test 4: make sure mark-done operation was called"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Already done @today @done", "tags": ["@today", "@done"], "subtasks": []}
            ]
        }
        batch_manager.batch_operation("testing.taskpaper", "@today", "mark-done", "batch")
        # test(s)
        mock_mark_done.assert_called_once_with("testing.taskpaper", "@today", "batch")

    @patch("src.managers.batch_manager.replace_tag")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.batch_manager.tag_mng.validate_tag", side_effect = ["@today", "@tomorrow"])
    def test_batch_call_replaceTag(self, mock_validate, mock_load, mock_replace_tag):
        """[batch replace-tag] Test 5: make sure replace-tag operation was called"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Already done @today @done", "tags": ["@today", "@done"], "subtasks": []}
            ]
        }
        batch_manager.batch_operation("testing.taskpaper", "@today", "replace-tag", "batch", "@tomorrow")
        # test(s)
        mock_replace_tag.assert_called_once_with("testing.taskpaper", "@today", "@tomorrow", "batch")

    @patch("src.managers.batch_manager.replace_tag")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.batch_manager.help_mng.show_error")
    def test_batch_replaceTag_noValue(self, mock_error, mock_load, mock_replace_tag):
        """[batch replace-tag] Test 6: no value provided for replace-tag action"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Already done @today @done", "tags": ["@today", "@done"], "subtasks": []}
            ]
        }
        batch_manager.batch_operation("testing.taskpaper", "@today", "replace-tag", "batch")
        # test(s)
        mock_error.assert_called_once_with("Error: Missing --value for <replace-tag> operation.")
        mock_replace_tag.assert_not_called()

    @patch("src.managers.batch_manager.replace_tag")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("src.managers.batch_manager.help_mng.show_error")
    def test_batch_unknownAction(self, mock_error, mock_load, mock_replace_tag):
        """[batch] Test 7: unknown action"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Already done @today @done", "tags": ["@today", "@done"], "subtasks": []}
            ]
        }
        batch_manager.batch_operation("testing.taskpaper", "@today", "unknown-action", "batch")
        # test(s)
        mock_error.assert_called_once_with("Unknown action: 'unknown-action'. Provide action from these choices: mark-done, replace-tag.")
        mock_replace_tag.assert_not_called()

    @patch("src.managers.batch_manager.help_mng.show_warning")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_batch_markDone_tagNotFound(self, mock_load, mock_warning):
        """[batch mark-done] Test 8: tag not found"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Already done @today @done", "tags": ["@today", "@done"], "subtasks": []}
            ]
        }
        batch_manager.mark_done("testing.taskpaper", "@important", "batch")
        # test(s)
        mock_warning.assert_called_once_with("Either no task with tag '@important' found or they're already marked done.")

    @patch("src.managers.batch_manager.help_mng.show_warning")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_batch_markDone_alreadyDone(self, mock_load, mock_warning):
        """[batch mark-done] Test 9: tag found but task already marked done"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Write report @important @done", "tags": ["@important", "@done"], "subtasks": []}
            ]
        }
        batch_manager.mark_done("testing.taskpaper", "@important", "batch")
        # test(s)
        mock_warning.assert_called_once_with("Either no task with tag '@important' found or they're already marked done.")

    @patch("src.managers.batch_manager.help_mng.show_warning")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_batch_eplaceTag_oldTagNotFound(self, mock_load, mock_warning):
        """[batch replace-tag] Test 10: filter tag not found"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Already done @today @done", "tags": ["@today", "@done"], "subtasks": []}
            ]
        }
        batch_manager.replace_tag("testing.taskpaper", "@important", "@tomorrow", "batch")
        # test(s)
        mock_warning.assert_called_once_with("Either no task with tag '@important' found or tag '@tomorrow' is already in the task name.")

    @patch("src.managers.batch_manager.help_mng.show_warning")
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    def test_batch_eplaceTag_newTagExists(self, mock_load, mock_warning):
        """[batch replace-tag] Test 11: filter tag is found but new tag already exists in the task name"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Write report @important @tomorrow", "tags": ["@important", "@tomorrow"], "subtasks": []}
            ]
        }
        batch_manager.replace_tag("testing.taskpaper", "@important", "@tomorrow", "batch")
        # test(s)
        mock_warning.assert_called_once_with("Either no task with tag '@important' found or tag '@tomorrow' is already in the task name.")

    @patch("src.managers.batch_manager.help_mng.show_success")
    @patch("managers.batch_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("managers.batch_manager.undo_mng.save_backup")
    def test_batch_markDone_success(self, mock_backup, mock_load, mock_write, mock_success):
        """[batch mark-done] Test 12: successfully marked done"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today", "tags": ["@today"], "subtasks": []},
                {"name": "Already done @today @done", "tags": ["@today", "@done"], "subtasks": []}
            ]
        }
        with patch("sys.stdout"):   # suppress printing
            batch_manager.mark_done("file.taskpaper", "@today", "batch")
        # test(s)
        self.assertIn("@today @done", batch_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"])  # task 1 marked done
        self.assertNotIn("@done @done", batch_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"])  # task 2 doesn't duplicate @done
        mock_backup.assert_called_once()
        mock_write.assert_called_once()
        mock_success.assert_called_once_with("All matching tasks are now marked as done.")

    @patch("src.managers.batch_manager.help_mng.show_success")
    @patch("managers.batch_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("managers.batch_manager.undo_mng.save_backup")
    def test_batch_replaceTag_success(self, mock_backup, mock_load, mock_write, mock_success):
        """[batch replace-tag] Test 13: successfully replaced tag"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {"name": "Fix bug @today @help", "tags": ["@today", "@help"], "subtasks": []},
                {"name": "Write report @today @important", "tags": ["@today", "@important"], "subtasks": []}
            ]
        }
        with patch("sys.stdout"):   # suppress printing
            batch_manager.replace_tag("file.taskpaper", "@today", "@important", "batch")
        # test(s)
        self.assertIn("@important", batch_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"])  # task 1 tag replaced
        self.assertNotIn("@today", batch_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"])  # task 1 tag replaced
        self.assertIn("@help", batch_manager.task_mng.loaded_taskpaper_data["Project A"][0]["name"])  # make sure other tag not affected
        self.assertIn("@today", batch_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"])  # task 2 tag doesn't get replaced
        self.assertIn("@important", batch_manager.task_mng.loaded_taskpaper_data["Project A"][1]["name"])  # task 2 tag doesn't get replaced
        mock_backup.assert_called_once()
        mock_write.assert_called_once()
        mock_success.assert_called_once_with("All matching tags have been replaced with '@important'.")

    @patch("src.managers.batch_manager.help_mng.show_success")
    @patch("managers.batch_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("managers.batch_manager.undo_mng.save_backup")
    def test_batch_markDone_subtask_success(self, mock_backup, mock_load, mock_write, mock_success):
        """[batch mark-done] Test 14: successfully marked done for sub-task"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {
                    "name": "Parent task", "tags": [],
                    "subtasks": [
                        {"name": "Child task @today @important", "tags": ["@today", "@important"], "subtasks": []}
                    ]
                }
            ]
        }
        with patch("sys.stdout"):   # suppress printing
            batch_manager.mark_done("file.taskpaper", "@today", "batch")
        # test(s)
        self.assertIn("@important @done", batch_manager.task_mng.loaded_taskpaper_data["Project A"][0]["subtasks"][0]["name"])  # sub-task marked done
        mock_backup.assert_called_once()
        mock_write.assert_called_once()
        mock_success.assert_called_once_with("All matching tasks are now marked as done.")

    @patch("src.managers.batch_manager.help_mng.show_success")
    @patch("managers.batch_manager.file_mng.write_taskpaper_file", return_value=True)
    @patch("src.managers.batch_manager.task_mng.load_taskpaper_data", return_value=True)
    @patch("managers.batch_manager.undo_mng.save_backup")
    def test_batch_replaceTag_subtask_success(self, mock_backup, mock_load, mock_write, mock_success):
        """[batch replace-tag] Test 15: successfully replaced tag for sub-task"""
        batch_manager.task_mng.loaded_taskpaper_data = {
            "Project A": [
                {
                    "name": "Parent task", "tags": [],
                    "subtasks": [
                        {"name": "Child task @today @important", "tags": ["@today", "@important"], "subtasks": []}
                    ]
                }
            ]
        }
        with patch("sys.stdout"):   # suppress printing
            batch_manager.replace_tag("file.taskpaper", "@today", "@tomorrow", "batch")
        # test(s)
        self.assertIn("@tomorrow @important", batch_manager.task_mng.loaded_taskpaper_data["Project A"][0]["subtasks"][0]["name"])  # sub-task marked done
        mock_backup.assert_called_once()
        mock_write.assert_called_once()
        mock_success.assert_called_once_with("All matching tags have been replaced with '@tomorrow'.")

if __name__ == "__main__":
    unittest.main()
