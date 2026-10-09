"""
helpers/help_manager.py
Help Manager - printing help and do error handling.
"""

from termcolor import colored
import difflib # for comparing sequences

printtab = "\t"
# printing help
def show_help(parser):
    """
    Display dynamically generated help message from the argument parser.
    """
    parser.print_help()

# printing error messages in red color for readability
def show_error(message):
    print(colored(message, 'red'))

# printing warning messages in yellow color for user experience
def show_warning(message):
    print(colored(message, 'yellow'))

# printing success messages in green color for user experience
def show_success(message):
    print(colored(message, 'green'))

# Autosuggestions for mistyped commands by suggesting the closest valid command
def suggest_command(user_command, valid_commands):
    # find 3 best matches with a loose similarity of 0.2 or more
    cmd_suggestions = difflib.get_close_matches(user_command, valid_commands, n=3, cutoff=0.2)
    if cmd_suggestions:
        return cmd_suggestions  # return the matches
    return None  # no good match found
