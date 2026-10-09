"""
cli/command_handler.py
Command Handler - Routes parsed commands to appropriate managers.
"""
import os
import sys

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from helpers import help_manager as help_mng
from managers import file_manager as file_mng
from managers import task_manager as task_mng
from managers import tag_manager as tag_mng
from managers import undo_manager as undo_mng
from managers import batch_manager as batch_mng

# Helper function for validating the opened file path
def isvalid_opened_file(opened_file_path):
    # check if there is a taskpaper file already opened
    if not opened_file_path:
        help_mng.show_error("No TaskPaper file is currently opened. Use the 'open' command first.")
        return False
    # check if the opened file path is valid
    elif not os.path.exists(opened_file_path):
        help_mng.show_error(f"The file '{opened_file_path}' does not exist. Please use the 'open' command first.")
        return False
    else:
        return True

# handling commands by routing them to managers
def handle_command(args, parser):
    # retrieve the file path from the temp file (if any)
    opened_file_path = file_mng.get_opened_file_path()
    # for 'create' subcommand    
    if args.command == "create":
        # use provided path (make it absolute path first) or default to current directory
        directory = os.path.abspath(args.path) if args.path else os.getcwd()
        file_mng.create_taskpaper_file(args.file_name, directory)
    # for 'open' subcommand    
    elif args.command == "open":
        file_mng.open_taskpaper_file(args.file_path)
    # for 'add-project' subcommand
    elif args.command == "add-project":
        # check if there is a valid taskpaper file already opened
        if isvalid_opened_file(opened_file_path):
            task_mng.add_project(opened_file_path, args.project_name, args.command)
    # for 'list-projects' subcommand
    elif args.command == "list-projects":
        if isvalid_opened_file(opened_file_path):
            task_mng.get_all_projects(opened_file_path)
    # for 'rename-project' subcommand
    elif args.command == "rename-project":
        if isvalid_opened_file(opened_file_path):
            task_mng.rename_project(opened_file_path, args.old_name, args.new_name, args.command)
    # for 'delete-project' subcommand
    elif args.command == "delete-project":
        if isvalid_opened_file(opened_file_path):
            task_mng.delete_project(opened_file_path, args.project_name, args.command)
    # for 'add-task' subcommand
    elif args.command == "add-task":
        if isvalid_opened_file(opened_file_path):
            task_mng.add_task(opened_file_path, args.project, args.task, args.command)
    # for 'list-tasks' subcommand
    elif args.command == "list-tasks":
        if not args.project and not args.tag:
            help_mng.show_error("Error: Either '--project' or '--tag' must be provided.")
        elif args.tag:
            if isvalid_opened_file(opened_file_path):
                tag_mng.list_tasks(opened_file_path, args.project, args.tag)
        else:
            if isvalid_opened_file(opened_file_path):
                task_mng.list_tasks(opened_file_path, args.project)
    # for 'edit-task' subcommand
    elif args.command == "edit-task":
        if isvalid_opened_file(opened_file_path):
            task_mng.edit_task(opened_file_path, args.project, args.command)
    # for 'delete-task' subcommand
    elif args.command == "delete-task":
        if isvalid_opened_file(opened_file_path):
            task_mng.delete_task(opened_file_path, args.project, args.command)
    # for 'move-task' subcommand
    elif args.command == "move-task":
        if isvalid_opened_file(opened_file_path):
            task_mng.move_task(opened_file_path, getattr(args, "from"), getattr(args, "to"), args.command)
    # for 'add-tag' subcommand
    elif args.command == "add-tag":
        if isvalid_opened_file(opened_file_path):
            tag_mng.add_tag(opened_file_path, args.project, args.tag_name, args.command)
    # for 'remove-tag' subcommand
    elif args.command == "remove-tag":
        if isvalid_opened_file(opened_file_path):
            tag_mng.remove_tag(opened_file_path, args.project, args.tag_name, args.command)
    # for 'list-tags' subcommand
    elif args.command == "list-tags":
        if isvalid_opened_file(opened_file_path):
            tag_mng.list_tags(opened_file_path, args.project)
    # for 'list-overdue' subcommand
    elif args.command == "list-overdue":
        if isvalid_opened_file(opened_file_path):
            tag_mng.list_overdue(opened_file_path, args.project)
    # for 'undo' subcommand
    elif args.command == "undo":
        if isvalid_opened_file(opened_file_path):
            undo_mng.undo_cmd(opened_file_path)
    # for 'batch' subcommand
    elif args.command == "batch":
        if isvalid_opened_file(opened_file_path):
            batch_mng.batch_operation(opened_file_path, args.filter, args.action, args.command, args.value)
    else:
        help_mng.show_help(parser)
