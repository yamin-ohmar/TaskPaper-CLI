"""
cli/argument_parser.py
Argument Parser - Validates and parses command-line arguments for TaskPaper CLI.
"""

import argparse
import importlib.metadata
from termcolor import colored

# adding arguments (subcommands/options) and their help descriptions
def parse_arguments():
    # a parser object to handle command-line arguments
    parser = argparse.ArgumentParser(prog='TaskPaper', description="TaskPaper Command-Line Interface Tool", formatter_class=argparse.RawTextHelpFormatter)

    # retrieve version from installed package metadata
    package_version = importlib.metadata.version("taskpaper-cli")

    # Command: "TaskPaper --version" - prints the version and exit by using 'action'
    parser.add_argument('-V', '--version', action='version', version=f"TaskPaper CLI {package_version}")

    # Add subparsers for subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Sub-command: Create (creating a taskpaper file)
    help_text_create = "Create a new TaskPaper file\nUsage:\t" + \
        colored("TaskPaper create <file_name> [-p <file_path>]", "green")

    create_parser = subparsers.add_parser("create", help=help_text_create)
    create_parser.add_argument("file_name", help="Name of the new TaskPaper file to be created")
    create_parser.add_argument("-p", "--path", help="File path to save the TaskPaper file")

    # Sub-command: Open (opening an existing taskpaper file)
    help_text_open = "Open to read a TaskPaper file\nUsage:\t" + \
        colored("TaskPaper open <file_path>", "green")

    open_parser = subparsers.add_parser("open", help=help_text_open)
    open_parser.add_argument("file_path", help="Path to the TaskPaper file to open")

    # Sub-command: add-project (adding new project)
    help_text_addProj = "Add a new project to the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper add-project <project_name>", "green")

    add_prj_parser = subparsers.add_parser("add-project", help=help_text_addProj)
    add_prj_parser.add_argument("project_name", help="Name of the new project to add")

    # Sub-command: list-projects (listing all projects)
    help_text_listProj = "List all projects from the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper list-projects", "green")
    
    ls_prj_parser = subparsers.add_parser("list-projects", help=help_text_listProj)

    # Sub-command: rename-project (renaming a project)
    help_text_renameProj = "Rename an existing project from the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper rename-project <old_name> <new_name>", "green")
    
    rename_prj_parser = subparsers.add_parser("rename-project", help=help_text_renameProj)
    rename_prj_parser.add_argument("old_name", help="The current name of the project to rename")
    rename_prj_parser.add_argument("new_name", help="The new name for the project")

    # Sub-command: delete-project (deleting a project)
    help_text_delProj = "Delete an existing project from the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper delete-project <project_name>", "green")

    del_prj_parser = subparsers.add_parser("delete-project", help=help_text_delProj)
    del_prj_parser.add_argument("project_name", help="Name of the new project to be deleted")

    # Sub-command: add-task (adding new task)
    help_text_addTask = "Add a new task to an existing project in the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper add-task -p <project> -t <task>", "green")
    
    add_task_parser = subparsers.add_parser("add-task", help=help_text_addTask)
    add_task_parser.add_argument('-p', '--project', required=True, help='The name of the project')
    add_task_parser.add_argument('-t', '--task', required=True, help='The name of the task to add')

    # Sub-command: list-tasks (listing all tasks)
    help_text_listTasks = "List tasks under a specific project or filter by a tag from the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper list-tasks -p <project>\n\t", "green") + \
        colored("TaskPaper list-tasks -t <@tag_name>\n\t", "green") + \
        colored("TaskPaper list-tasks -p <project> -t <@tag_name>", "green")
    
    ls_task_parser = subparsers.add_parser("list-tasks", help=help_text_listTasks)
    ls_task_parser.add_argument('-p', '--project', required=False, help='The name of the project whose tasks to be listed')
    ls_task_parser.add_argument('-t', '--tag', required=False, help='Filter tasks containing the given tag')

    # Sub-command: edit-task (editing a task)
    help_text_editTask = "Edit an existing task under a specific project interactively\nUsage:\t" + \
        colored("TaskPaper edit-task -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index> <updated_task>", "green")
    
    desc_text_editTask = "Flow:\t" + \
        colored("TaskPaper edit-task -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index> <updated_task>", "green")
    
    edit_task_parser = subparsers.add_parser("edit-task", description=desc_text_editTask, help=help_text_editTask,
                                             formatter_class=argparse.RawTextHelpFormatter)
    edit_task_parser.add_argument('-p', '--project',required=True, help='The name of the project where the task is located')

    # Sub-command: delete-task (deleting a task)
    help_text_delTask = "Delete an existing task under a specific project interactively\nUsage:\t" + \
        colored("TaskPaper delete-task -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    desc_text_delTask = "Flow:\t" + \
        colored("TaskPaper delete-task -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    delete_task_parser = subparsers.add_parser("delete-task", description=desc_text_delTask, help=help_text_delTask,
                                             formatter_class=argparse.RawTextHelpFormatter)
    delete_task_parser.add_argument('-p', '--project',required=True, help='The name of the project where the task is located')

    # Sub-command: move-task (moving a task from project to project)
    help_text_moveTask = "Move an existing task under a specific project to another project interactively\nUsage:\t" + \
        colored("TaskPaper move-task --from <source_project> --to <destination_project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    desc_text_moveTask = "Flow:\t" + \
        colored("TaskPaper move-task --from <source_project> --to <destination_project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    move_task_parser = subparsers.add_parser("move-task", description=desc_text_moveTask, help=help_text_moveTask,
                                             formatter_class=argparse.RawTextHelpFormatter)
    move_task_parser.add_argument('--from',required=True, help='The name of the project where task is currently in')
    move_task_parser.add_argument('--to',required=True, help='The name of the project where task is to be moved to')

    # Sub-command: add-tag (adding a tag to a task)
    help_text_addTag = "Add a tag to an existing task under a specific project interactively\nUsage:\t" + \
        colored("TaskPaper add-tag <@tag_name> -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    desc_text_addTag = "Flow:\t" + \
        colored("TaskPaper add-tag <@tag_name> -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    add_tag_parser = subparsers.add_parser("add-tag", description=desc_text_addTag, help=help_text_addTag,
                                             formatter_class=argparse.RawTextHelpFormatter)
    add_tag_parser.add_argument("tag_name", help="Name of the tag to be added to the task")
    add_tag_parser.add_argument('-p', '--project',required=True, help='The name of the project where the task is located')

    # Sub-command: remove-tag (removing a tag from a task)
    help_text_removeTag = "Remove a tag from an existing task under a specific project interactively\nUsage:\t" + \
        colored("TaskPaper remove-tag <@tag_name> -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    desc_text_removeTag = "Flow:\t" + \
        colored("TaskPaper remove-tag <@tag_name> -p <project>\n", "green") + \
        "\tA list of tasks will be listed with a prompt\n\tKey in:\t" + \
        colored("<task_index>", "green")
    
    remove_tag_parser = subparsers.add_parser("remove-tag", description=desc_text_removeTag, help=help_text_removeTag,
                                             formatter_class=argparse.RawTextHelpFormatter)
    remove_tag_parser.add_argument("tag_name", help="Name of the tag to be removed from the task")
    remove_tag_parser.add_argument('-p', '--project',required=True, help='The name of the project where the task is located')

    # Sub-command: list-tags (listing all unique tags in a project)
    help_text_listTags = "List all unique tags available under a specific project from the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper list-tags -p <project>", "green")
    
    ls_tag_parser = subparsers.add_parser("list-tags", help=help_text_listTags)
    ls_tag_parser.add_argument('-p', '--project', required=True, help='The name of the project whose tags are to be listed')

    # Sub-command: list-overdue (listing all overdue tasks)
    help_text_listOverdue = "List all overdue tasks from the currently opened TaskPaper file\nUsage:\t" + \
        colored("TaskPaper list-overdue\n\t", "green") + \
        colored("TaskPaper list-overdue -p <project>", "green")
    
    ls_overdue_parser = subparsers.add_parser("list-overdue", help=help_text_listOverdue)
    ls_overdue_parser.add_argument('-p', '--project', required=False, help='The name of the project whose overdue tasks are to be listed')

    # Sub-command: undo (undo previous command)
    help_text_undo = "Undo previous action that altered the Taskpaper file\nUsage:\t" + \
        colored("TaskPaper undo", "green")
    
    subparsers.add_parser("undo", help=help_text_undo)

    # Sub-command: batch (batch operations for similar tasks)
    help_text_batch = "Perform batch operations on tasks filtered by a single tag\nUsage:\t" + \
        colored("TaskPaper batch -f <@tag_name> -a <operation> [-v <optional_value>]\n\t", "green") + \
        "operation choices:\t" + \
        colored("mark-done, replace-tag", "green")
    
    batch_parser = subparsers.add_parser("batch", help=help_text_batch)
    batch_parser.add_argument('-f', '--filter', required=True, help="Filter tasks with tags (e.g., @today, @priority(high), @done)")
    batch_parser.add_argument('-a', '--action', required=True, choices=["mark-done", "replace-tag"], help="Batch action to perform on the filtered tasks")
    batch_parser.add_argument('-v', '--value', help="Value used in the action (e.g., @newtag for replace-tag)")

    return parser
