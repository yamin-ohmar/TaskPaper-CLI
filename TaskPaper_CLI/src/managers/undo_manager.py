"""
managers/undo_manager.py
Undo Manager - Handles saving the last state of the taskpaper file before any modification.
             - Handles restoring the last state of the taskpaper file when undo is called.
"""

import sys
import os
import tempfile
import shutil # library for file operations (copying)

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from helpers import help_manager as help_mng
from managers import task_manager as task_mng

# define the path for the temporary file (to store last backup file path)
TEMP_UNDO_FILE = os.path.join(tempfile.gettempdir(), ".taskpaper_undo")

# Save backup file (as the last state of taskpaper file) before any modifications
def save_backup(filepath, command):
    backup_filepath = filepath + ".bak"  # a backup file path with (.bak) at the end
    # copy the original taskpaper file contents to create a backup file
    shutil.copy(filepath, backup_filepath)
    
    # store the last backup file path
    try:
        with open(TEMP_UNDO_FILE, "w") as f:
            f.write(f"{backup_filepath}\n{command}")  # store path + command/action
    except Exception as e:
        raise RuntimeError(f"Failed to save the backup file path. Reason: {e}")

# Undo function to undo the last action done on the taskpaper file (if any)
def undo_cmd(filepath):
    # read temporary file for backup file information
    if os.path.exists(TEMP_UNDO_FILE):
        try:
            with open(TEMP_UNDO_FILE, "r") as f:
                lines = f.readlines()
                if len(lines) < 2: # should have 2 lines stored
                    help_mng.show_error("Invalid undo data.")
                    return False
                backup_filepath = lines[0].strip()  # 1st line: backup file path
                command = lines[1].strip()  # 2nd line: command
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve backup file path. Reason: {e}")

        # confirmation for undo
        confirmation = task_mng.std_input(f"Are you sure you want to undo the last action ('{command}')? (y/n): ").strip().lower()
        if confirmation != 'y':
            help_mng.show_warning("Undo cancelled.")
            return

        # check if the backup file exists
        if os.path.exists(backup_filepath):
            # restore the backup data into the original taskpaper file
            shutil.copy(backup_filepath, filepath)
            # only one time Undoing is allowed
            os.remove(backup_filepath)  # delete the backup file after restoring
            os.remove(TEMP_UNDO_FILE)  # delete the temp file with undo file info
            
            help_mng.show_success(f"Undo successful: Restored '{filepath}' after '{command}'.")
        else:
            help_mng.show_error(f"The backup file '{backup_filepath}' does not exist.")
    else:
        help_mng.show_warning("Nothing to undo.")
