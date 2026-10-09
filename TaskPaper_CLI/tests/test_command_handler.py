"""
tests/test_command_handler.py

Purpose:
    - This testing script is to do unit testing (automated testing) for 
    src/cli/command_handler.py file.
    - To check isvalid_opened_file() function.

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_command_handler.py"
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
from unittest.mock import patch, MagicMock

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.cli import command_handler

class TestCommandHandler(unittest.TestCase):

    # using a mock object for show_error() function from help_manager.py 
    @patch("cli.command_handler.help_mng.show_error")
    def test_isvalid_opened_file_none(self, mock_show_error):
        """[command_handler.py] Test 1: no file is opened"""
        result = command_handler.isvalid_opened_file(None)
        # making sure show_error func was called exactly once with below error message as argument 
        mock_show_error.assert_called_once_with("No TaskPaper file is currently opened. Use the 'open' command first.")
        self.assertFalse(result)    # expected it to be False

    # using a mock object for show_error() function from help_manager.py 
    @patch("cli.command_handler.help_mng.show_error")
    def test_isvalid_opened_file_invalid_path(self, mock_show_error):
        """[command_handler.py] Test 2: file path does not exist"""
        result = command_handler.isvalid_opened_file("nonexistent.taskpaper")
        # making sure show_error func was called exactly once with below error message as argument 
        mock_show_error.assert_called_once_with("The file 'nonexistent.taskpaper' does not exist. Please use the 'open' command first.")
        self.assertFalse(result)    # expected it to be False

    def test_isvalid_opened_file_valid_path(self):
        """[command_handler.py] Test 3: file path exists"""
        # create dummy taskpaper file just for testing
        with open("temp.taskpaper", "w") as f:
            f.write("Sample content")
        result = command_handler.isvalid_opened_file("temp.taskpaper")
        # delete the dummy taskpaper file after testing
        os.remove("temp.taskpaper")
        self.assertTrue(result) # expected it to be True

if __name__ == "__main__":
    unittest.main()
