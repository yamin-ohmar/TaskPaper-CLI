"""
managers/batch_manager.py
Batch Operation Manager - Handles certain bulk operations on tasks filtered by specific tag.
"""

import sys
import os
import re

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from helpers import help_manager as help_mng
from managers import task_manager as task_mng
from managers import tag_manager as tag_mng
from managers import undo_manager as undo_mng
from managers import file_manager as file_mng

"""
Action Handlers
"""

# Action handling function to add "@done" tag for all tasks with given tag
def mark_done(filepath, filter_tag, command):
    modified = False
    filterTag_small = filter_tag.lower()

    # iterate for each task in the whole taskpaper file
    for project, tasks in task_mng.loaded_taskpaper_data.items():
        # recursive function to search for matching tasks and update with "@done" tag
        def searchAndUpdate(tasks):
            nonlocal modified   # to update in this function
            for task in tasks:
                task_tags = [tag.lower() for tag in task["tags"]]  # get tags from task and convert to lowercase
                # add "@done" tag only if the task matches with filtering tag and "@done" is not already added
                if filterTag_small in task_tags and "@done" not in task_tags:
                    task["name"] = task["name"].strip() + " @done"
                    modified = True
                # do recursion for subtasks (if any)
                if task["subtasks"]:
                    searchAndUpdate(task["subtasks"])
        searchAndUpdate(tasks)

    # if there is at lease one task being updated
    if modified:
        # save a backup for undo
        undo_mng.save_backup(filepath, command)
        # inform about the adding of tag "@done"
        print(f"Adding tag '@done' to tasks with tag '{filter_tag}' in file '{filepath}'...")
        # write data back to the file and check if it is successful
        if file_mng.write_taskpaper_file(filepath, task_mng.loaded_taskpaper_data):
            help_mng.show_success("All matching tasks are now marked as done.")
    else:
        help_mng.show_warning(f"Either no task with tag '{filter_tag}' found or they're already marked done.")

# Action handling function to replace the filtering tag with the given tag value
def replace_tag(filepath, old_tag, new_tag, command):
    modified = False
    oldTag_small = old_tag.lower()
    newTag_small = new_tag.lower()

    # iterate for each task in the whole taskpaper file
    for project, tasks in task_mng.loaded_taskpaper_data.items():
        # recursive function to search for matching tasks and update with given value (new tag)
        def searchAndUpdate(tasks):
            nonlocal modified   # to update in this function
            for task in tasks:
                task_tags = [tag.lower() for tag in task["tags"]]  # get tags from task and convert to lowercase
                if oldTag_small in task_tags and newTag_small not in task_tags:
                    # replace old tag in task name with new tag (using regular expressing to find all regardless of case)
                    task["name"] = re.sub(re.escape(old_tag), new_tag, task["name"], flags=re.IGNORECASE)
                    modified = True
                # do recursion for subtasks (if any)
                if task["subtasks"]:
                    searchAndUpdate(task["subtasks"])
        searchAndUpdate(tasks)

    # if there is at lease one task being updated
    if modified:
        # save a backup for undo
        undo_mng.save_backup(filepath, command)
        # inform about the replacing of tag
        print(f"Replacing tag '{old_tag}' with '{new_tag}' in file '{filepath}'...")
        # write data back to the file and check if it is successful
        if file_mng.write_taskpaper_file(filepath, task_mng.loaded_taskpaper_data):
            help_mng.show_success(f"All matching tags have been replaced with '{new_tag}'.")
    else:
        help_mng.show_warning(f"Either no task with tag '{old_tag}' found or tag '{new_tag}' is already in the task name.")

"""
End of Action Handlers
"""

# Batch operation function
def batch_operation(filepath, filter_tag, action, command, value=None):
    # check if the data is loaded in memory
    if not task_mng.load_taskpaper_data(filepath):
        return
    
    # check if the given tag is valid
    valid_tag = tag_mng.validate_tag(filter_tag, check_duedate=True)
    if not valid_tag:
        return

    # dispatch to the correct action handler
    if action == "mark-done":
        mark_done(filepath, valid_tag, command)
    elif action == "replace-tag":
        if not value:
            help_mng.show_error("Error: Missing --value for <replace-tag> operation.")
            return
        valid_new_tag = tag_mng.validate_tag(value, check_duedate=True)
        if not valid_new_tag:
            return
        replace_tag(filepath, valid_tag, valid_new_tag, command)
    else:
        help_mng.show_error(f"Unknown action: '{action}'. Provide action from these choices: mark-done, replace-tag.")
