"""
tests/test_argument_parser.py

Purpose:
    - This testing script is to do unit testing (automated testing) for 
    src/cli/argument_parser.py file.
    - To check whether the text inputs are being parsed as CLI arguments correctly.

Testing:
    - To activate the virtual environment (venv) created by pipx for taskpaper-cli:
        "source /Users/yaminohmar/.local/pipx/venvs/taskpaper-cli/bin/activate"
    - To execute this unit test script inside this activated virtual environment:
        "python -m unittest tests/test_argument_parser.py"
    - [Alternatively] To execute all unit test files inside this venv:
        "python -m unittest discover -s tests"
    - To deactivate this venv after testing:
        "deactivate"

Author: Yamin Ohmar
University: University of Leicester
"""

import unittest
import sys
import os

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from src.cli.argument_parser import parse_arguments

class TestArgumentParser(unittest.TestCase):

    def test_argparse_create(self):
        """[argument_parser.py] Test 1: for 'create' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["create", "My Tasks", "--path", "/Users/yaminohmar/Downloads/projects"])
        # tests
        self.assertEqual(args.file_name, "My Tasks")
        self.assertEqual(args.path, "/Users/yaminohmar/Downloads/projects")
    
    def test_argparse_create_shorthand(self):
        """[argument_parser.py] Test 2: for 'create' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["create", "My Tasks", "-p", "/Users/yaminohmar/Documents/projects"])
        # tests
        self.assertEqual(args.file_name, "My Tasks")
        self.assertEqual(args.path, "/Users/yaminohmar/Documents/projects")

    def test_argparse_open(self):
        """[argument_parser.py] Test 3: for 'open' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["open", "/Users/yaminohmar/Downloads/projects/My Tasks.taskpaper"])
        # tests
        self.assertEqual(args.file_path, "/Users/yaminohmar/Downloads/projects/My Tasks.taskpaper")

    def test_argparse_addProject(self):
        """[argument_parser.py] Test 4: for 'add-project' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["add-project", "Project Y"])
        # tests
        self.assertEqual(args.project_name, "Project Y")

    def test_argparse_listProjects(self):
        """[argument_parser.py] Test 5: for 'list-projects' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["list-projects"])
        # tests
        self.assertEqual(args.command, "list-projects")

    def test_argparse_renameProject(self):
        """[argument_parser.py] Test 6: for 'rename-project' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["rename-project", "Project Y", "Project X"])
        # tests
        self.assertEqual(args.old_name, "Project Y")
        self.assertEqual(args.new_name, "Project X")

    def test_argparse_deleteProject(self):
        """[argument_parser.py] Test 7: for 'delete-project' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["delete-project", "Project Z"])
        # tests
        self.assertEqual(args.project_name, "Project Z")

    def test_argparse_addTask(self):
        """[argument_parser.py] Test 8: for 'add-task' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["add-task", "--project", "Project X", "--task", "Write tests"])
        # tests
        self.assertEqual(args.project, "Project X")
        self.assertEqual(args.task, "Write tests")

    def test_argparse_addTask_shorthand(self):
        """[argument_parser.py] Test 9: for 'add-task' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["add-task", "-p", "Project Y", "-t", "Execute tests"])
        # tests
        self.assertEqual(args.project, "Project Y")
        self.assertEqual(args.task, "Execute tests")

    def test_argparse_listTasks(self):
        """[argument_parser.py] Test 10: for 'list-tasks' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["list-tasks", "--project", "Project Z", "--tag", "@urgent"])
        # tests
        self.assertEqual(args.project, "Project Z")
        self.assertEqual(args.tag, "@urgent")

    def test_argparse_listTasks_shorthand(self):
        """[argument_parser.py] Test 11: for 'list-tasks' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["list-tasks", "-p", "Project A", "-t", "@priority(high)"])
        # tests
        self.assertEqual(args.project, "Project A")
        self.assertEqual(args.tag, "@priority(high)")

    def test_argparse_editTask(self):
        """[argument_parser.py] Test 12: for 'edit-task' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["edit-task", "--project", "Project X"])
        # tests
        self.assertEqual(args.project, "Project X")

    def test_argparse_editTask_shorthand(self):
        """[argument_parser.py] Test 13: for 'edit-task' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["edit-task", "-p", "Project Y"])
        # tests
        self.assertEqual(args.project, "Project Y")

    def test_argparse_deleteTask(self):
        """[argument_parser.py] Test 14: for 'delete-task' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["delete-task", "--project", "Project Y"])
        # tests
        self.assertEqual(args.project, "Project Y")

    def test_argparse_deleteTask_shorthand(self):
        """[argument_parser.py] Test 15: for 'delete-task' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["delete-task", "-p", "Project X"])
        # tests
        self.assertEqual(args.project, "Project X")

    def test_argparse_moveTask(self):
        """[argument_parser.py] Test 16: for 'move-task' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["move-task", "--from", "Project Z", "--to", "Project A"])
        # tests
        self.assertEqual(getattr(args, "from"), "Project Z")
        self.assertEqual(getattr(args, "to"), "Project A")

    def test_argparse_addTag(self):
        """[argument_parser.py] Test 17: for 'add-tag' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["add-tag", "@help", "--project", "Project B"])
        # tests
        self.assertEqual(args.tag_name, "@help")
        self.assertEqual(args.project, "Project B")

    def test_argparse_addTag_shorthand(self):
        """[argument_parser.py] Test 18: for 'add-tag' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["add-tag", "@urgent", "-p", "Project C"])
        # tests
        self.assertEqual(args.tag_name, "@urgent")
        self.assertEqual(args.project, "Project C")

    def test_argparse_removeTag(self):
        """[argument_parser.py] Test 19: for 'remove-tag' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["remove-tag", "@important", "--project", "Project X"])
        # tests
        self.assertEqual(args.tag_name, "@important")
        self.assertEqual(args.project, "Project X")

    def test_argparse_removeTag_shorthand(self):
        """[argument_parser.py] Test 20: for 'remove-tag' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["remove-tag", "@due(2025-03-22)", "-p", "Project Y"])
        # tests
        self.assertEqual(args.tag_name, "@due(2025-03-22)")
        self.assertEqual(args.project, "Project Y")

    def test_argparse_listTags(self):
        """[argument_parser.py] Test 21: for 'list-tags' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["list-tags", "--project", "Project A"])
        # tests
        self.assertEqual(args.project, "Project A")

    def test_argparse_listTags_shorthand(self):
        """[argument_parser.py] Test 22: for 'list-tags' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["list-tags", "-p", "Project Z"])
        # tests
        self.assertEqual(args.project, "Project Z")

    def test_argparse_listOverdue(self):
        """[argument_parser.py] Test 23: for 'list-overdue' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["list-overdue", "--project", "Project Z"])
        # tests
        self.assertEqual(args.project, "Project Z")

    def test_argparse_listOverdue_shorthand(self):
        """[argument_parser.py] Test 24: for 'list-overdue' command (shorthand)"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["list-overdue", "-p", "Project B"])
        # tests
        self.assertEqual(args.project, "Project B")

    def test_argparse_undo(self):
        """[argument_parser.py] Test 25: for 'undo' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["undo"])
        # tests
        self.assertEqual(args.command, "undo")

    def test_argparse_batchMarkDone(self):
        """[argument_parser.py] Test 26: for 'mark-done' operation of 'batch' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["batch", "--filter", "@today", "--action", "mark-done"])
        # tests
        self.assertEqual(args.filter, "@today")
        self.assertEqual(args.action, "mark-done")
        self.assertEqual(args.value, None)

    def test_argparse_batchReplaceTag(self):
        """[argument_parser.py] Test 27: for 'replace-tag' operation of 'batch' command"""
        parser = parse_arguments()
        # inputs
        args = parser.parse_args(["batch", "--filter", "@today", "--action", "replace-tag", "--value", "@tomorrow"])
        # tests
        self.assertEqual(args.filter, "@today")
        self.assertEqual(args.action, "replace-tag")
        self.assertEqual(args.value, "@tomorrow")

if __name__ == "__main__":
    unittest.main()