"""
managers/task_manager.py
Task Manager - Handles data operations related to projects and tasks in a TaskPaper file.
"""

import sys
import os

from termcolor import colored

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from helpers import help_manager as help_mng
from managers import file_manager as file_mng
from managers import undo_manager as undo_mng

# Global variable to store the loaded TaskPaper data
loaded_taskpaper_data = {}  # Example: {'Project Name': [Task objects list]} - as dictionary

"""
Helper Functions
"""

# Helper function to load taskpaper data
def load_taskpaper_data(filepath):
    global loaded_taskpaper_data # updating this global variable in this function
    # if the file is not parsed into memory yet, do it now
    if not loaded_taskpaper_data:
        try:
            with open(filepath, "r") as file:
                loaded_taskpaper_data = file_mng.parse_taskpaper_file(file.read())
                return True
        except Exception as e:
            help_mng.show_error(f"Error: Unable to load data from file '{filepath}'. Reason: {e}")
            return False

# Helper function to check if the project really exists
def isPrj_exist(project, filepath):
    if project not in loaded_taskpaper_data:
        help_mng.show_error(f"Error: Project '{project}' does not exist in file '{filepath}'.")
        return False
    else:
        return True

# Helper function to display tasks under a specific project
def display_project_tasks(filepath, project_name):
    # Inner Function: display tasks with flattened indexes while maintaining indentation for readability
    def display_indexed_tasks(tasks, indexed_tasks, indent_level=0):
        for task in tasks:
            indexed_tasks.append(task)  # store tasks in a new list
            index = len(indexed_tasks)  # use length of the list as its index
            indent = "\t" * indent_level  # use appropriate no. of tabs for indentation
            print(f"{indent}{index}. {task['name']}")   # print with indentation for readablity (for sub-tasks)

            # recursively display subtasks (if any)
            if task["subtasks"]:
                display_indexed_tasks(task["subtasks"], indexed_tasks, indent_level + 1) # increase the indentation

    # main function starts here
    project_name = project_name.strip()
    # check if the project name is empty
    if not project_name:
        help_mng.show_error("Error: Invalid project name. The name cannot be empty.")
        return None
    # check if the project really exists
    if not isPrj_exist(project_name, filepath):
        return None

    # get the list of tasks from the project
    tasks = loaded_taskpaper_data[project_name]
    if not tasks:
        help_mng.show_warning(f"There are no tasks under project '{project_name}' in file '{filepath}'.")
        return None

    # display tasks
    indexed_tasks = []
    print(f"Tasks in project '{project_name}':")
    display_indexed_tasks(tasks, indexed_tasks)

    return indexed_tasks

# Helper function to extract info separately 
def parse_edit_input(user_input):
    try:
        # split the input into index and text
        index, new_text = user_input.split(" ", 1)
        return int(index), new_text.strip('" ')
    except (ValueError, IndexError):
        raise ValueError("Invalid input. Format should be: <index> \"<updated text>\"")

# Helper function to recursively find a task inside `loaded_taskpaper_data` and returns its reference
def find_task_in_memory(task_list, target_task):
    for task in task_list:
        if task is target_task:  # check if it's the same object reference
            return task
        # recursively finding if task not found yet
        found_task = find_task_in_memory(task["subtasks"], target_task)
        if found_task:
            return found_task
    return None  # task not found

# Helper function to make sure interactive prompts work properly on all 3 OS (Windows, Mac, Linux)
def std_input(prompt):
    colored_prompt = colored(prompt, "cyan")
    print(colored_prompt, end=' ', flush=True)  # to keep user input on the same line
    return input()

"""
End of Helper Functions
"""

# Add a new project to the opened TaskPaper file
def add_project(filepath, project_name, command):
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return
    project_name = project_name.strip()
    # check if the project name is empty
    if not project_name:
        help_mng.show_error("Error: Invalid project name. The name cannot be empty.")
    # check if the project is in the existing data
    elif project_name in loaded_taskpaper_data:
        help_mng.show_warning(f"Project '{project_name}' already exists.")
    else:
        # saving backup data of the previous state first
        undo_mng.save_backup(filepath, command)

        # then add the project to memory data
        loaded_taskpaper_data[project_name] = []
        print(f"Adding project '{project_name}' to file '{filepath}'...")
        # write data back to the file and check if it is successful
        if (file_mng.write_taskpaper_file(filepath, loaded_taskpaper_data)):
            help_mng.show_success(f"Added project '{project_name}' successfully.")

# List all projects from the opened TaskPaper file
def get_all_projects(filepath):
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return
    projects = list(loaded_taskpaper_data.keys())
    # check if there are any projects
    if not projects:
        help_mng.show_warning(f"There are no project in file '{filepath}'.")
    else:
        # use enumerate for indexing (index starts at 1)
        for index, project in enumerate(projects, start=1):
            print(f"{index}.{help_mng.printtab}{project}")
        help_mng.show_success(f"A total of {index} project(s) listed from file '{filepath}'.")

# Rename an existing project to a new name
def rename_project(filepath, old_name, new_name, command):
    global loaded_taskpaper_data # updating this global variable in this function
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return

    old_name = old_name.strip()
    new_name = new_name.strip()
    
    # check if the old/new project name is empty
    if not old_name or not new_name:
        help_mng.show_error("Error: Invalid project name(s). The name(s) cannot be empty.")
        return
    # check if the project really exists
    if not isPrj_exist(old_name, filepath):
        return
    # check if the new name is the same as the old name
    if new_name == old_name:
        help_mng.show_warning("Project name remains the same. No changes made.")
        return
    # check if the new project name already exists
    if new_name in loaded_taskpaper_data:
        help_mng.show_warning(f"Project '{new_name}' already exists in file '{filepath}'. \nPlease choose a different name.")
        return
    
    # renaming the project while preserving the original order of projects 
    ordered_prjs = list(loaded_taskpaper_data.items())
    for index, (prj_name, tasks) in enumerate(ordered_prjs):
        if prj_name == old_name:
            ordered_prjs[index] = (new_name, tasks)  # rename the project and assign its tasks back
            break
    
    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    # rebuild the dictionary after renaming project orderly
    loaded_taskpaper_data = dict(ordered_prjs)
    print(f"Renaming project '{old_name}' to '{new_name}' in file '{filepath}'...")
    
    # write data back to the file and check if it is successful
    if file_mng.write_taskpaper_file(filepath, loaded_taskpaper_data):
        help_mng.show_success(f"Successfully renamed project '{old_name}' to '{new_name}'.")

def delete_project(filepath, project_name, command):
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return
    project_name = project_name.strip()

    # check if the project name is empty
    if not project_name:
        help_mng.show_error("Error: Invalid project name. The name cannot be empty.")
        return
    
    # check if the project really exists
    if not isPrj_exist(project_name, filepath):
        return
    
    # confirmation for deletion
    confirmation = std_input(f"Are you sure you want to delete the entire project: '{project_name}'? (y/n): ").strip().lower()
    if confirmation != 'y':
        help_mng.show_warning("Project deletion cancelled.")
        return

    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    # delete project
    del loaded_taskpaper_data[project_name]
    print(f"Deleting the project '{project_name}' in file '{filepath}'...")
    
    # write data back to the file and check if it is successful
    if (file_mng.write_taskpaper_file(filepath, loaded_taskpaper_data)):
        help_mng.show_success(f"Successfully deleted the project '{project_name}'.")

# Add a new task to the existing project in the opened TaskPaper file
def add_task(filepath, project_name, task_name, command):
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return

    # get rid of extra spaces (beginning and trailing)
    project_name = project_name.strip()
    task_name = task_name.strip()

    # check if the project name or task name is empty
    if not project_name or not task_name:
        help_mng.show_error("Error: Invalid project name (or) task name. The name(s) cannot be empty.")
        return
    
    # check if the project really exists
    if not isPrj_exist(project_name, filepath):
        return
    
    # get the list of tasks from the project
    tasks = loaded_taskpaper_data[project_name]

    # check if the task already exists in that tasks list
    if any(task["name"] == task_name for task in tasks):
        help_mng.show_warning(f"Task '{task_name}' already exists in project '{project_name}'.")
        return
    
    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    # add the task to the project's tasks list with an empty subtasks list
    new_task = {"name": task_name, "subtasks": []}
    tasks.append(new_task)
    print(f"Adding task '{task_name}' to project '{project_name}' in file '{filepath}'...")
    
    # write data back to the file and check if it is successful
    if (file_mng.write_taskpaper_file(filepath, loaded_taskpaper_data)):
        help_mng.show_success(f"Added task '{task_name}' successfully.")

# List tasks under a project from the opened TaskPaper file
def list_tasks(filepath, project_name):
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return
    # use helper function to display tasks
    indexed_tasks = display_project_tasks(filepath, project_name)
    if indexed_tasks:
        help_mng.show_success(f"A total of {len(indexed_tasks)} task(s) listed for project '{project_name}' from file '{filepath}'.")

# Edit task under a project from the opened TaskPaper file
def edit_task(filepath, project_name, command):
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return
    indexed_tasks = display_project_tasks(filepath, project_name)
    if not indexed_tasks:
        return  # exit if there are no tasks or the project is invalid

    # prompt user for input (for interactive experience)
    try:
        user_input = std_input("\nPlease key in the index of the task to be edited and the updated text for that task (e.g., 2 \"Updated Task Text\"): ")
        index, new_text = parse_edit_input(user_input)
    except ValueError as e:
        help_mng.show_error(str(e))
        return

    # check index for validation
    if index < 1 or index > len(indexed_tasks):
        help_mng.show_error(f"Error: Invalid index. Must be from 1 to {len(indexed_tasks)}.")
        return
    
    # check if the new task name is empty
    if not new_text:
        help_mng.show_error("Error: Invalid updated text. The new task name cannot be empty.")
        return

    # locate the old task from memory and get its reference
    old_task = indexed_tasks[index - 1] # get old task
    task_to_update = find_task_in_memory(loaded_taskpaper_data[project_name], old_task)

    # if no task found in memory data structure
    if not task_to_update:
        help_mng.show_error(f"Error: Could not locate task in project '{project_name}'.")
        return
    
    # check if the new task is the same as the old task
    if new_text == old_task['name']:
        help_mng.show_warning(f"Task name remains the same. No changes made.")
        return

    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    print(f"Updating the task '{old_task['name']}' to '{new_text}' in file '{filepath}'...")
    # Update the old task reference with the new task name while keeping its subtasks intact
    task_to_update["name"] = new_text # set new task
    
    # write data back to the file and check if it is successful
    if (file_mng.write_taskpaper_file(filepath, loaded_taskpaper_data)):
        help_mng.show_success(f"Task successfully updated in project '{project_name}'.")

# Delete task under a project from the opened TaskPaper file
def delete_task(filepath, project_name, command):
    # Inner Function: remove task from its parent list
    def remove_task_from_memory(task_list, target_task):
        for index, task in enumerate(task_list):
            if task is target_task:
                del task_list[index]  # remove task by index to get its sub-tasks too
                return True
            # recursively check subtasks if not found yet
            if remove_task_from_memory(task["subtasks"], target_task):
                return True
        return False  # task not found
    
    # main function starts here
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return
    indexed_tasks = display_project_tasks(filepath, project_name)
    if not indexed_tasks:
        return  # exit if there are no tasks or the project is invalid

    # prompt user for input (for interactive experience)
    try:
        index = int(std_input("\nPlease key in the index of the task to be deleted (e.g., 2): "))
    except ValueError:
        help_mng.show_error("Invalid input. Please enter a number.")
        return

    # check index for validation
    if index < 1 or index > len(indexed_tasks):
        help_mng.show_error(f"Error: Invalid index. Must be from 1 to {len(indexed_tasks)}.")
        return

    # confirmation for deletion
    task_to_delete = indexed_tasks[index - 1]
    confirmation = std_input(f"Are you sure you want to delete task '{task_to_delete['name']} and its sub-tasks (if any)'? (y/n): ").strip().lower()
    if confirmation != 'y':
        help_mng.show_warning("Task deletion cancelled.")
        return

    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    # delete the task and all its subtasks
    if remove_task_from_memory(loaded_taskpaper_data[project_name], task_to_delete):
        print(f"Deleting the task '{task_to_delete['name']}' and its sub-tasks (if any) in file '{filepath}'...")
    else:
        help_mng.show_error("Error: Task could not be removed.")
        return
    
    # write data back to the file and check if it is successful
    if (file_mng.write_taskpaper_file(filepath, loaded_taskpaper_data)):
        help_mng.show_success(f"Task successfully deleted in project '{project_name}'.")

# Move task under a project to another project
def move_task(filepath, from_project, to_project, command):
    # Inner Function: remove task from its parent list
    def move_task_in_memory(source_list, dest_list, target_task):
        for index, task in enumerate(source_list):
            if task is target_task:
                dest_list.append(target_task)  # add task to destination project
                del source_list[index]  # remove task by index to get its sub-tasks too
                return True
            # recursively check subtasks if not found yet
            if move_task_in_memory(task["subtasks"], dest_list, target_task):
                return True
        return False  # task not found
    
    # main function starts here
    # check if the data is loaded in memory
    if not load_taskpaper_data(filepath):
        return
    # check if the destination project name is empty
    to_project = to_project.strip()
    if not to_project:
        help_mng.show_error("Error: Invalid project name. The name cannot be empty.")
        return
    # check if the destination project really exists
    if not isPrj_exist(to_project, filepath):
        return
    # check if the source project is the same as the destination project
    from_project = from_project.strip()
    if from_project == to_project:
        help_mng.show_warning(f"Source project name and destination project name are the same. No changes made.")
        return
    # display a list of tasks from the source project
    indexed_tasks = display_project_tasks(filepath, from_project)
    if not indexed_tasks:
        return  # exit if there are no tasks or the project is invalid
    
    # prompt user for input (for interactive experience)
    try:
        index = int(std_input("\nPlease key in the index of the task to be moved (e.g., 2): "))
    except ValueError:
        help_mng.show_error("Invalid input. Please enter a number.")
        return

    # check index for validation
    if index < 1 or index > len(indexed_tasks):
        help_mng.show_error(f"Error: Invalid index. Must be from 1 to {len(indexed_tasks)}.")
        return

    # confirmation for moving
    task_to_move = indexed_tasks[index - 1]
    confirmation = std_input(f"Are you sure you want to move task '{task_to_move['name']}' and its sub-tasks (if any) to project '{to_project}'? (y/n): ").strip().lower()
    if confirmation != 'y':
        help_mng.show_warning("Task moving cancelled.")
        return

    # saving backup data of the previous state first
    undo_mng.save_backup(filepath, command)

    # move the task to the destination project and delete it from the source project
    if move_task_in_memory(loaded_taskpaper_data[from_project], loaded_taskpaper_data[to_project], task_to_move):
        print(f"Moving the task '{task_to_move['name']}' and its sub-tasks (if any) to project '{to_project}' in file '{filepath}'...")
    else:
        help_mng.show_error("Error: Task could not be moved.")
        return
    
    # write data back to the file and check if it is successful
    if (file_mng.write_taskpaper_file(filepath, loaded_taskpaper_data)):
        help_mng.show_success(f"Task successfully moved from project '{from_project}' to project '{to_project}'.")
