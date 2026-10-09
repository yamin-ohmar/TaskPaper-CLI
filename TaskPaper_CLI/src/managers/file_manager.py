"""
managers/file_manager.py
File Manager - Handles file operations like creating TaskPaper files.
"""

import json
import os
import sys
import re
import tempfile

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from helpers import help_manager as help_mng

# define the path for the temporary file (to store opened file path)
TEMP_DATA_FILE = os.path.join(tempfile.gettempdir(), ".taskpaper_tempdata")

# Helper function to save the currently opened file path to a temporary file
def save_opened_file_path(filepath):
    try:
        with open(TEMP_DATA_FILE, "w") as f:
            f.write(filepath)
            help_mng.show_success(f"Successfully loaded filepath '{filepath}' into memory.")
    except Exception as e:
        raise RuntimeError(f"Failed to save opened file path. Reason: {e}")

# Helper function to retrieve the currently opened file path to a temporary file
def get_opened_file_path():
    if os.path.exists(TEMP_DATA_FILE):
        try:
            with open(TEMP_DATA_FILE, "r") as f:
                return f.read().strip()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve opened file path. Reason: {e}")
    return None

# Helper function to cleanup file name using RegEx
def cleanup_filename(filename):
    # replace invalid chars with underscore and also set the char length
    return re.sub(r'[<>:"/\\|?*]', '_', filename)[:255]

# Helper function to validate directory and creates it
def validate_directory(directory):
    try: # check if it can be created
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except OSError as e: # if not, show error to users with reason
        help_mng.show_error(f"Error: Unable to create or access directory '{directory}'. Reason: {e}")
        return False
    
"""
Structured Dictionary: (in memory - parsed from TaskPaper file) 
{
    "Project X": [                                      # name = project name, value = list of its task                                               # (nesting tasks: max level 3)
        {
            "name": "Task 1",                           # name = name, value = task name (Level 1)
            "tags": [],
            "subtasks": [                               # name = subtasks, value = list of its sub-tasks
                {
                    "name": "Subtask 1.1 @tag1 @tag2",  # same format as tasks (Level 2)
                    "tags": ["@tag1", "@tag2"],
                    "subtasks": [
                        {
                            "name": "Subtask 1.1.1",    # same format as tasks (Level 3)
                            "tags": [],
                            "subtasks": []              # empty list for subtasks
                        },
                        {
                            "name": "Subtask 1.1.2 @tag3",    # same format as tasks (Level 3)
                            "tags": ["@tag3"],
                            "subtasks": []                    # empty list for subtasks
                        },
                    ]
                },
                {
                    "name": "Subtask 1.2",
                    "tags": [],
                    "subtasks": []
                }
            ]
        },
        {
            "name": "Task 2",
            "tags": [],
            "subtasks": []
        }
    ]
}
"""
# Helper function to parse TaskPaper file content into structured dictionary
def parse_taskpaper_file(content):
    taskpaper_data = {}
    current_project = None
    task_stack = []  # to track nesting
    prev_indent = 0  # to track previous indentation level

    for line in content.splitlines():
        stripped_line = line.strip()
        indent_level = (len(line) - len(stripped_line)) # spaces = indentation level (current)

        # project line detection (ends with ":")
        if stripped_line.endswith(":") and not stripped_line.startswith("- "):
            current_project = stripped_line[:-1].strip()    # remove ":" at the end
            taskpaper_data[current_project] = []
            task_stack = []  # reset stack
            prev_indent = 0  # reset indentation tracking

        # task or sub-task line detection (starts with "- ")
        elif stripped_line.lstrip().startswith("- "):
            task_name = stripped_line.lstrip()[2:].strip()  # remove "- " prefix
            
            # extract words starting with "@" using RegEx
            tags = re.findall(r"@\S+", task_name)   # '\S' get string w/o space, '+' one/more occurance
            
            # extract @due(yyyy-mm-dd) from tags list
            duedate = None
            due_date_pattern = re.compile(r"@due\((\d{4}-\d{2}-\d{2})\)", re.IGNORECASE)  # Regex pattern for @due(yyyy-mm-dd)
            for tag in tags:
                match = due_date_pattern.match(tag) # check regex pattern and return a match obj
                if match:
                    duedate = match.group(1)  # extract due date from obj ('1' gets the 1st parenthesized subgroup)
                    break  # stop after finding the first valid due date
            
            # extract priority from tags list
            priority = None
            priority_pattern = re.compile(r"@priority\((high|medium|low)\)", re.IGNORECASE)  # Regex pattern for @priority(...)
            short_priority_pattern = re.compile(r"@(high|medium|low)", re.IGNORECASE)  # Regex pattern for @high, @medium, @low
            for tag in tags:
                match = priority_pattern.match(tag) or short_priority_pattern.match(tag)
                if match:
                    priority = match.group(1).lower()  # set to lowercase
                    break  # stop after finding the first valid priority
            
            # store in dictionary format
            task_entry = {
                "name": task_name, 
                "tags": tags, 
                "duedate": duedate, 
                "priority": priority,
                "subtasks": []
                }

            if current_project:
                if indent_level == 1:  # level 1 (main task)
                    taskpaper_data[current_project].append(task_entry)
                    task_stack = [task_entry]  # reset stack with new task
                else:
                    # limit the indentation levels up to 3 (not to stress the system)
                    if len(task_stack) <= 0:
                        help_mng.show_error("The formatting of the opened TaskPaper file content has some issues. Please check the file.\nHint: Sub-tasks without main task.")
                        return
                    elif len(task_stack) >= 3 or indent_level <= prev_indent:
                        task_stack.pop()  # to merge level 4+ into level 3

                    task_stack[-1]["subtasks"].append(task_entry)  # add as subtask
                    task_stack.append(task_entry)  # tracking in stack
            else:
                help_mng.show_error("The formatting of the opened TaskPaper file content has some issues. Please check the file.\nHint: Tasks without project.")
                return

            prev_indent = indent_level  # update previous indent
    
    # print(json.dumps(taskpaper_data, indent=4)) # checking memory structure
    return taskpaper_data

"""
Structured TaskPaper Format: (in file - serialized from system's memory data) 
Project X:
    - Task 1
        - Task 1.1 @tag1 @tag2
            - Task 1.1.1
            - Task 1.1.2 @tag3
        - Task 1.2
    - Task 2
"""
# Helper function to serialize dictionary (data) back to TaskPaper file format
def serialize_taskpaper_data(data):
    # Inner Function: write task lines
    def write_tasks(tasks, indent=1):
        lines = []
        for task in tasks:
            # print the name of the task with indentation and a "-"
            disp_indent = help_mng.printtab * indent
            lines.append(f"{disp_indent}- {task['name']}")
            # nesting up to level 3 only (not to stress the system)
            if indent < 3 and task["subtasks"]: 
                lines.extend(write_tasks(task["subtasks"], indent + 1)) # recursion
            # merge level 4+ into level 3
            elif indent >= 3 and task["subtasks"]:
                for subtask in task["subtasks"]:
                    lines.append(f"{disp_indent}- {subtask['name']}")
        return lines
    
    # main function starts here
    lines = []
    for project, tasks in data.items():
        lines.append(f"{project}:")  # add back each project name with a colon
        # use extend instead of append to avoid nested list when it returns from inner function
        lines.extend(write_tasks(tasks, indent=1)) # call inner function to write tasks
        lines.append("")  # a blank line for spacing between projects
    return "\n".join(lines)  # Join all lines with newline characters

# creating empty taskpaper files
def create_taskpaper_file(filename, directory):
    # validate filename
    filename = cleanup_filename(filename)
    filename = filename.strip()
    if not filename:
        help_mng.show_error("Error: Invalid file name. The name cannot be empty.")
        return
    
    # Add file extension (.taskpaper)
    if not filename.endswith('.taskpaper'):
        filename += '.taskpaper'

    # validate directory
    if not validate_directory(directory):
        return

     # full path for the file
    filepath = os.path.join(directory, filename)
    absolute_filepath = os.path.abspath(filepath)
    
    # create the file
    file = None
    try:
        file = open(filepath, "x")
        file.write("")
        help_mng.show_success(f"TaskPaper file '{absolute_filepath}' has been created.")
    except FileExistsError: # if the file already exists
        help_mng.show_error(f"Error: '{absolute_filepath}' file already exists.")
    except Exception as e:
        help_mng.show_error(f"{e}")
    finally: # close the file if it was successfully opened
        if file is not None:
            file.close()

# opening and reading existing TaskPaper files
def open_taskpaper_file(filepath):
    # eliminate files with empty file path
    filepath = filepath.strip()
    if not filepath:
        help_mng.show_error("Error: Invalid file path. The path cannot be empty.")
        return
    else:
        # make it absolute path first
        filepath = os.path.abspath(filepath)
    
    # check if it has a `.taskpaper` extension
    if not filepath.endswith('.taskpaper'):
        help_mng.show_warning("Please provide a valid TaskPaper file with the correct '.taskpaper' extension (e.g., tasks.taskpaper).")
        return
    
    # check if it points to a valid file
    if not os.path.isfile(filepath):
        help_mng.show_error(f"Error: File '{filepath}' does not exist or is not accessible.")
        return

    save_opened_file_path(filepath) # Save the file path for subsequence commands

# writing edited data into existing taskpaper file
def write_taskpaper_file(filepath, data):
    try:
        with open(filepath, "w") as file:
            # write back all data into the opened taskpaper file
            serialized_content = serialize_taskpaper_data(data)
            file.write(serialized_content)
            return True
    except Exception as e:
        help_mng.show_error(f"Error: Unable to write to file '{filepath}'. Reason: {e}")
        return False
