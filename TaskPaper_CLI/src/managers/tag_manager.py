"""
managers/tag_manager.py
Tag Manager - Handles data operations related to tags in a TaskPaper file.
"""

import re
import sys
import os

from tabulate import tabulate
from datetime import datetime, timedelta
from termcolor import colored

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from helpers import help_manager as help_mng
from managers import file_manager as file_mng
from managers import task_manager as task_mng
from managers import undo_manager as undo_mng

"""
Helper Functions
"""
done_tags = {"@done", "@completed", "@finished"}    # as a set
priority_level = {"high": 1, "medium": 2, "low": 3, None: 4}    # dict to map priority to numerical values

# Helper function to check the tag validity
def validate_tag(tag_name, check_duedate):
    valid_tag = ""
    tag_name = tag_name.strip()

    # check the tag (ensure only one "@" and it is at the beginning)
    if "@" in tag_name and not tag_name.startswith("@"):
        help_mng.show_error("Error: A tag must start with '@' or not contain '@' at all.")
        return valid_tag
    stripped_tag_name = tag_name.lstrip("@")    # removing all "@"

    # check if the tag name is empty
    if not stripped_tag_name:
        help_mng.show_error("Error: Invalid tag. The tag name cannot be empty.")
        return valid_tag

    # ensure tag name is a single word
    if re.search(r"\s", stripped_tag_name): # '\s' get string with spaces
        help_mng.show_error("Error: A tag must be a single word without spaces.")
        return valid_tag
    
    tag_name = f"@{stripped_tag_name}"  # add back '@' at the beginning

    # Regex pattern for valid due date: @due(yyyy-mm-dd)
    due_date_pattern = re.compile(r"^@due\(\d{4}-\d{2}-\d{2}\)$")   # '$' to strickly enforce it ends with just that

    # ensure due date tag is in correct taskpaper date format
    if check_duedate and tag_name.lower().startswith("@due("):
        if not due_date_pattern.match(tag_name):
            help_mng.show_error("Error: Invalid due date format. Please use '@due(YYYY-MM-DD)'.")
            return valid_tag
    
    valid_tag = tag_name
    return valid_tag

# Helper funciton to get a set of unique tags under a project
def extractUniqueTags(tasks):
    unique_tags = set() # set: to make sure no duplicates
    for task in tasks:
        tags = re.findall(r"@\S+", task["name"])
        unique_tags.update(tags)
        # recursively check subtasks (if any)
        if task["subtasks"]:
            unique_tags.update(extractUniqueTags(task["subtasks"]))
    return unique_tags

# # Helper function to check if a task is due on a specific date
# def isTaskDueAt(task, tag_name):
#     if not task["duedate"]:  # ensure 'duedate' exists
#         return False
#     tag_due_date = tag_name[5:-1]  # extract date from "@due(YYYY-MM-DD)" by slicing
#     try:
#         tag_due_date = datetime.strptime(tag_due_date, "%Y-%m-%d").date()   # strap date from the filtering tag
#         task_due_date = datetime.strptime(task["duedate"], "%Y-%m-%d").date()  # strap date from task's duedate key
#         return task_due_date == tag_due_date  # compare the dates
#     except ValueError:
#         return False  # for all invalid date formats

# Helper function to check if a task is due today
def isTaskDueToday(task):
    if not task["duedate"]:  # ensure 'duedate' exists
        return False
    try:
        task_due_date = datetime.strptime(task["duedate"], "%Y-%m-%d").date()  # strap date from @due tag
        return task_due_date == datetime.today().date()  # compare with today's date
    except ValueError:
        return False  # for all invalid date formats

# Helper function to check if a task is overdue
def isTaskOverdue(duedate):
    if not duedate:  # ensure 'duedate' exists
        return False
    try:
        task_due_date = datetime.strptime(duedate, "%Y-%m-%d").date()  # strap date from @due tag
        return task_due_date <= datetime.today().date()  # any task that is older than today
    except ValueError:
        return False  # for all invalid date formats
    
# Helper function to check if a task due in a week 
def isTaskDueInAWeek(duedate):
    if not duedate:  # ensure 'duedate' exists
        return False
    try:
        task_due_date = datetime.strptime(duedate, "%Y-%m-%d").date()  # strap date from @due tag
        # return bool after checking if due date is in a week (7 days) from now
        return task_due_date <= datetime.today().date() + timedelta(days=7)
    except ValueError:
        return False  # for all invalid date formats

# Helper function to filter tasks based on a tag and return them in a structured format
def filter_tasks(tasks, project_name, tag_name):
    filtered_tasks = []

    # recursive function to search for matching tasks
    def search_tasks(tasks, project_name, tag_name):
        for task in tasks:
            task_tags = [tag.lower() for tag in task["tags"]]  # get tags from task and convert to lowercase
            tagName_small = tag_name.lower()
            
            # filter all due dates
            if tagName_small == "@due":
                if task['duedate']: # check if there is duedate key 
                    filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])

            # # filter by specific due date
            # elif tagName_small.startswith("@due("):
            #     if isTaskDueAt(task, tag_name):
            #         filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])

            # filtering today's tasks
            elif tagName_small == "@today":
                # check tasks with "@today" tag and @due(YYYY-MM-DD) tag with today's date
                if "@today" in task_tags or isTaskDueToday(task):
                    filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])
            
            # filtering all priority tasks
            elif tagName_small == "@priority":
                if task['priority']:
                    filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])
            
            # filtering high priority tasks
            elif tagName_small == "@priority(high)" or tagName_small == "@high":
                if task['priority'] == "high":
                    filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])

            # filtering medium priority tasks
            elif tagName_small == "@priority(medium)" or tagName_small == "@medium":
                if task['priority'] == "medium":
                    filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])

            # filtering low priority tasks
            elif tagName_small == "@priority(low)" or tagName_small == "@low":
                if task['priority'] == "low":
                    filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])

            # filtering completed tasks
            elif tagName_small in done_tags:
                # check with set intersection
                if done_tags & set(task_tags):
                    filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])
            
            # handling other tags
            elif tagName_small in task_tags: # check if they're in tags key
                filtered_tasks.append([project_name, task["name"], task["tags"], task["duedate"], task["priority"]])

            # checking subtasks recursively
            if task["subtasks"]:
                search_tasks(task["subtasks"], project_name, tag_name)

        return

    # searching tasks
    search_tasks(tasks, project_name, tag_name)
    return filtered_tasks

# Helper function to filter overdue tasks based on its "@due(YYYY-MM-DD)" tag
def filter_overdue_tasks(tasks, project_name):
    overdue_tasks = []

    # recursive function to search for overdue tasks
    def search_odTasks(tasks, project_name):
        for task in tasks:
            task_tags = [tag.lower() for tag in task["tags"]]  # get tags from task and convert to lowercase
            if isTaskOverdue(task["duedate"]) and "@done" not in task_tags: # check if the task is overdue and not done yet
                overdue_tasks.append([project_name, task["name"], task["priority"]])
            # checking subtasks recursively
            if task["subtasks"]:
                search_odTasks(task["subtasks"], project_name)
        return

    # searching overdue tasks
    search_odTasks(tasks, project_name)
    return overdue_tasks

# Helper function for color legends
def print_colorLegend():
    # displays color legend before printing the task table
    print("\n" + "="*40)
    print(" Task Color Legend:")
    print(f"{help_mng.printtab}{colored('Completed tasks', 'green')}")
    print(f"{help_mng.printtab}{colored('Tasks due within a week', 'yellow')}")
    print(f"{help_mng.printtab}{colored('Overdue tasks', 'red')}")
    print(f"{help_mng.printtab}Tasks far from due dates")
    print("="*40 + "\n")

# Helper function to print tasks in a table format with colors
def print_table_colored(taskslist):
    colored_tasks = []
    print_colorLegend() # information about color formatting

    # helper function for coloring tasks based on the due dates
    def color_task (task_name, tags, duedate):
        # color green for completed tasks
        if done_tags & set(tags):
            return colored(task_name, "green")
        # color red for overdue tasks
        if isTaskOverdue(duedate):
            return colored(task_name, "red")
        # color yellow for tasks due in a week
        if isTaskDueInAWeek(duedate):
            return colored(task_name, "yellow")
        return task_name
    
    # apply color formatting and also indexing starting from 1
    for index, (prj, task, tags, due, priority) in enumerate(taskslist, start=1):
        colored_tasks.append([index, prj, color_task(task, tags, due), priority])
    
    tasklis_headers = ["No.", "Project", "Task Name", "Priority"]   # headers
    print(tabulate(colored_tasks, tasklis_headers, tablefmt="rst") + "\n")   # printing simple table with headers

# Helper function to print tasks in a table format without colors
def print_table(taskslist, task_header):
    indexed_tasks = []
    # indexing starting from 1 (*task = expanding the list of a task)
    for index, task in enumerate(taskslist, start=1):
        indexed_tasks.append([index, *task])

    tasklis_headers = ["No.", "Project", task_header, "Priority"]   # headers
    print("\n" + tabulate(indexed_tasks, tasklis_headers, tablefmt="rst") + "\n")   # printing simple table with headers

"""
End of Helper Functions
"""

# Add a new tag to the chosen task
def add_tag(filepath, project_name, tag_name, command):
    # check if the given tag is valid
    valid_tag = validate_tag(tag_name, check_duedate=True)
    if not valid_tag:
        return
    
    # check if the data is loaded in memory
    if not task_mng.load_taskpaper_data(filepath):
        return
    
    # display tasks for user selection
    indexed_tasks = task_mng.display_project_tasks(filepath, project_name)
    if not indexed_tasks:
        return  # exit if there are no tasks or the project is invalid
    
    # prompt user for input (for interactive experience)
    try:
        index = int(task_mng.std_input("\nPlease key in the index of the task for tag to be added (e.g., 2): "))
    except ValueError:
        help_mng.show_error("Invalid input. Please enter a number.")
        return
    
    # check index for validation
    if index < 1 or index > len(indexed_tasks):
        help_mng.show_error(f"Error: Invalid index. Must be from 1 to {len(indexed_tasks)}.")
        return
    
    # locate the selected task from memory and get its reference
    selected_task = indexed_tasks[index - 1]
    task_to_update = task_mng.find_task_in_memory(task_mng.loaded_taskpaper_data[project_name], selected_task)

    # if no task found in memory data structure
    if not task_to_update:
        help_mng.show_error(f"Error: Could not locate task in project '{project_name}'.")
        return

    # check if the same tag already exists in the task
    if valid_tag in task_to_update["tags"]:
        help_mng.show_warning(f"Task '{task_to_update['name']}' already has the tag '{valid_tag}'.")
        return
    
    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    # adding the tag to the task
    print(f"Adding tag '{valid_tag}' to task '{task_to_update['name']}' under project '{project_name}' in file '{filepath}'...")
    task_to_update["name"] += f" {valid_tag}"

    # write data back to the file and check if it is successful
    if (file_mng.write_taskpaper_file(filepath, task_mng.loaded_taskpaper_data)):
        help_mng.show_success(f"Tag successfully added to task: '{task_to_update['name']}'.")

# Remove a tag from a chosen task
def remove_tag(filepath, project_name, tag_name, command):
    # check if the given tag is valid
    valid_tag = validate_tag(tag_name, check_duedate=False)
    if not valid_tag:
        return

    # check if the data is loaded in memory
    if not task_mng.load_taskpaper_data(filepath):
        return
    
    # display tasks for user selection
    indexed_tasks = task_mng.display_project_tasks(filepath, project_name)
    if not indexed_tasks:
        return  # exit if there are no tasks or the project is invalid
    
    # prompt user for input (for interactive experience)
    try:
        index = int(task_mng.std_input("\nPlease key in the index of the task to remove the tag from (e.g., 2): "))
    except ValueError:
        help_mng.show_error("Invalid input. Please enter a number.")
        return

    if index < 1 or index > len(indexed_tasks):
        help_mng.show_error(f"Error: Invalid index. Must be from 1 to {len(indexed_tasks)}.")
        return

    # locate the selected task from memory and get its reference
    selected_task = indexed_tasks[index - 1]
    task_to_update = task_mng.find_task_in_memory(task_mng.loaded_taskpaper_data[project_name], selected_task)

    # if no task found in memory data structure
    if not task_to_update:
        help_mng.show_error(f"Error: Could not locate task in project '{project_name}'.")
        return
    
    # check if the tag exists in the task
    if valid_tag not in task_to_update["tags"]:
        help_mng.show_warning(f"The task '{task_to_update['name']}' does not contain the tag '{valid_tag}'.")
        return

    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    # removing the tag from the task
    print(f"Removing tag '{valid_tag}' from task '{task_to_update['name']}' under project '{project_name}' in file '{filepath}'...")
    task_to_update["name"] = task_to_update["name"].replace(f"{valid_tag}", "").strip()
    
    # write data back to the file and check if it is successful
    if (file_mng.write_taskpaper_file(filepath, task_mng.loaded_taskpaper_data)):
        help_mng.show_success(f"Tag successfully removed from task: '{task_to_update['name']}'.")

# List all unique tags under a project from the opened TaskPaper file
def list_tags(filepath, project_name):
    # check if the data is loaded in memory
    if not task_mng.load_taskpaper_data(filepath):
        return
    # check if the project name is empty
    project_name = project_name.strip()
    if not project_name:
        help_mng.show_error("Error: Invalid project name. The name cannot be empty.")
        return
    # check if the project really exists
    if not task_mng.isPrj_exist(project_name, filepath):
        return
    
    # get all unique tags in a set from a project
    unique_tags = extractUniqueTags(task_mng.loaded_taskpaper_data[project_name])
    # display all unique tags
    if not unique_tags:
        help_mng.show_warning(f"No tags found in project '{project_name}'.")
    else:
        print(f"\nUnique tags used in project '{project_name}':")
        # print by sorting (A-Z first then a-z)
        for index, tag in enumerate(sorted(unique_tags), start=1):
            print(f"{index}.{help_mng.printtab}{tag}")
        help_mng.show_success(f"A total of {index} unique tags used in project '{project_name}' from file '{filepath}'.")

# Filter tasks with a tag from the opened TaskPaper file
def list_tasks(filepath, project_name=None, tag_name=None):
    # check if the data is loaded in memory
    if not task_mng.load_taskpaper_data(filepath):
        return
        
    # check if the given tag is valid
    valid_tag = validate_tag(tag_name, check_duedate=True)
    if not valid_tag:
        return
    taskslist = []  # empty task list for filtered tasks

    # if only [--tag] argument is provided in command-line
    if tag_name and not project_name:
        for project, tasks in task_mng.loaded_taskpaper_data.items():
            filteredTasks = filter_tasks(tasks, project, valid_tag)
            taskslist.extend(filteredTasks)

    # if both [--tag] and [--project] arguments are provided
    elif tag_name and project_name:
        project_name = project_name.strip()
        # check if the project name is empty
        if not project_name:
            help_mng.show_error("Error: Invalid project name. The name cannot be empty.")
            return
        # check if the project really exists
        if not task_mng.isPrj_exist(project_name, filepath):
            return
        taskslist = filter_tasks(task_mng.loaded_taskpaper_data[project_name], project_name, valid_tag)

    # Sorting: using lambda function to lookup priority levels, and sort the list by that value as a key
    sorted_taskslist = sorted(taskslist, key=lambda task: priority_level[task[4]])  # task's priority at index 4

    # display filtered tasks in table format
    if sorted_taskslist:
        print_table_colored(sorted_taskslist)
        help_mng.show_success(f"A total of {len(sorted_taskslist)} task(s) listed from file '{filepath}'.")
    else:
        help_mng.show_warning("No matching tasks found.")

# List overdue tasks from the opened TaskPaper file
def list_overdue(filepath, project_name=None):
    # check if the data is loaded in memory
    if not task_mng.load_taskpaper_data(filepath):
        return
    taskslist = []  # empty task list for filtered tasks

    # if [--project] argument is not provided in command-line
    if not project_name:
        for project, tasks in task_mng.loaded_taskpaper_data.items():
            overdueTasks = filter_overdue_tasks(tasks, project)
            taskslist.extend(overdueTasks)
    else:
        project_name = project_name.strip()
        # check if the project name is empty
        if not project_name:
            help_mng.show_error("Error: Invalid project name. The name cannot be empty.")
            return
        # check if the project really exists
        if not task_mng.isPrj_exist(project_name, filepath):
            return
        taskslist = filter_overdue_tasks(task_mng.loaded_taskpaper_data[project_name], project_name)

    # Sorting: using lambda function to lookup priority level, and sort the list by that value as a key
    sorted_taskslist = sorted(taskslist, key=lambda task: priority_level[task[2]])  # task's priority at index 2

    # display overdue tasks in table format
    if sorted_taskslist:
        print_table(sorted_taskslist, "Overdue Task(s)")
        help_mng.show_success(f"A total of {len(sorted_taskslist)} overdue task(s) listed from file '{filepath}'.")
    else:
        help_mng.show_warning("No overdue tasks found.")
