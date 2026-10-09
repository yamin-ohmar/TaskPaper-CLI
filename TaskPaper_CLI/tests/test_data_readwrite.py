"""
tests/test_data_readwrite.py

Purpose:
    - This testing script is to do unit testing (automated testing) for 
    TaskPaper data parsing (reading) and data serialization (writing).
    - By checking serialize_taskpaper_data() and parse_taskpaper_file() 
    functions from src/cli/file_manager.py.

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_data_readwrite.py"
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
from unittest.mock import mock_open, patch

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.managers import file_manager

class TestFileManager(unittest.TestCase):

    def test_serialize_data_simple(self):
        """[data_read_write] Test 1: serialize a simple TaskPaper structure"""
        data = {
            "Project A": [
                {"name": "Task 1 @done", "tags": ["@done"], "subtasks": []},
                {"name": "Task 2", "tags": [], "subtasks": []}
            ]
        }

        # making sure it serializes project and task names in correct format
        result = file_manager.serialize_taskpaper_data(data)
        self.assertIn("Project A:", result)
        self.assertIn("- Task 1 @done", result)
        self.assertIn("- Task 2", result)

    def test_serialize_data_nested(self):
        """[data_read_write] Test 2: serialize a nested TaskPaper structure"""
        nested_data = {
            "Project B": [
                {
                    "name": "Main Task",
                    "tags": [],
                    "subtasks": [
                        {
                            "name": "Subtask 1 @today",
                            "tags": ["@today"],
                            "subtasks": [
                                {
                                    "name": "Sub-subtask 1.1",
                                    "tags": [],
                                    "subtasks": []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # making sure it serializes project and task names in correct format
        result = file_manager.serialize_taskpaper_data(nested_data)
        self.assertIn("Project B:", result)
        self.assertIn("- Main Task", result)
        self.assertIn("\t- Subtask 1 @today", result)
        self.assertIn("\t\t- Sub-subtask 1.1", result)

    def test_parse_basic_structure(self):
        """[data_read_write] Test 3: parse a nested TaskPaper structure"""
        nested_content = """Project A:
 - Task 1 @done
 - Task 2 @due(2025-05-01)
  - Subtask 2.1 @priority(high)
   - Sub-subtask 2.1.1 @medium

Project B:
 - Task 3"""

        # making sure the it parses project and task names in correct format
        result = file_manager.parse_taskpaper_file(nested_content)

        # check projects
        self.assertIn("Project A", result)
        self.assertIn("Project B", result)

        # check Task 1
        task1 = result["Project A"][0]
        self.assertEqual(task1["name"], "Task 1 @done")
        self.assertIn("@done", task1["tags"])
        self.assertEqual(task1["subtasks"], [])

        # check Task 2 and its subtasks
        task2 = result["Project A"][1]
        self.assertEqual(task2["name"], "Task 2 @due(2025-05-01)")
        self.assertEqual(task2["duedate"], "2025-05-01")
        self.assertEqual(len(task2["subtasks"]), 1)

        subtask = task2["subtasks"][0]
        self.assertEqual(subtask["priority"], "high")
        self.assertIn("@priority(high)", subtask["tags"])

        nested_subtask = subtask["subtasks"][0]
        self.assertIn("@medium", nested_subtask["tags"])
        self.assertEqual(nested_subtask["priority"], "medium")

        # check Project B
        task3 = result["Project B"][0]
        self.assertEqual(task3["name"], "Task 3")

if __name__ == "__main__":
    unittest.main()
