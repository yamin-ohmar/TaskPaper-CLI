"""
cli/main.py
TaskPaper CLI - Main Entry Point
Handles user input and initializes argument parsing and command handling.
"""
# To allow running as an executable
#!/usr/bin/env python3

import os
import sys

# importing own modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from cli import argument_parser as arg_parser
from cli import command_handler as cmd_handler
from helpers import help_manager as help_mng

def main():
    # Manually take user command when provided
    if len(sys.argv) > 1:
        user_command = sys.argv[1] # get the user command at index 1

        # only if it is not a flag (e.g. '-h' or '-v')
        if not user_command.startswith("-"):
            # all the valid commands as implemented in argument_parser.py
            valid_commands = [
                "create", "open", "add-project", "list-projects", "rename-project", "delete-project",
                "add-task", "list-tasks", "edit-task", "delete-task", "move-task",
                "add-tag", "remove-tag", "list-tags", "list-overdue", "undo", "batch"
            ]

            # when the user's command is not in the valid commands list
            if user_command not in valid_commands:
                # inform about unknown command
                help_mng.show_error(f"\nCommand not recognized: '{user_command}'")

                # check if they meant help or version
                if user_command == "help":
                    help_mng.show_warning("Run 'TaskPaper -h' for help.\n")
                    sys.exit(1) # quit the program
                elif user_command == "ver" or user_command == "version":
                    help_mng.show_warning("Run 'TaskPaper -v' for version.\n")
                    sys.exit(1) # quit the program

                # if not, look for the best match
                suggestions = help_mng.suggest_command(user_command, valid_commands)
                if suggestions: # if there is a match
                    if len(suggestions) == 1:   # if only one match
                        help_mng.show_warning(f"Do you mean: '{suggestions[0]}'?\n")
                    else:   # if more than one match
                        help_mng.show_warning("Do you mean one of these commands?")
                        for cmd in suggestions:
                            help_mng.show_warning(f"  - {cmd}")
                        print()
                    sys.exit(1) # quit the program
                else:
                    help_mng.show_warning("Run 'TaskPaper -h' to see all the available commands and their usages.\n")
                    sys.exit(1) # quit the program

    # proceed only when the command is valid
    # Parse user inputs
    parser = arg_parser.parse_arguments()
    args = parser.parse_args()

    # Route commands
    cmd_handler.handle_command(args, parser)

if __name__ == "__main__":
    main()
