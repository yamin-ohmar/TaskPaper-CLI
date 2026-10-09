# TaskPaper Command-Line Interface (CLI)

 > By Yamin Ohmar

## Overview

TaskPaper CLI is a cross-platform command-line application developed in Python for managing tasks and projects stored in TaskPaper (`.taskpaper`) files. It provides an interactive way to organise tasks, manage tags, and perform operations on multiple tasks without requiring a graphical interface.

### Key Features

- **File management:** Create and open TaskPaper files.
- **Project management:** Add, rename and delete projects.
- **Task management:** Add, edit, move and delete tasks.
- **Tag management:** Add, remove and list tags.
- **Task tracking:** List tasks and identify overdue tasks.
- **Batch operations:** Apply supported changes to multiple tasks at once.
- **Undo:** Reverse the most recent supported operation.
- **Interactive CLI:** Guided prompts and helpful command feedback.

## 1. Contents in this repository

### 1.1. TaskPaper CLI Tool (Code related items)
1. **Source Code** 
- In the folder: `TaskPaper_CLI > src`
2. **Installation Files (Distribution Files)**
- In the folder: `TaskPaper_CLI > dist`
- Latest release: `taskpaper_cli-1.0.0-py3-none-any.whl`
3. **Automated Testing Scripts (Unit Testing Files)**
- In the folder: `TaskPaper_CLI > tests`


### 1.2. Documentations
1. **Design Documents (for each command)**
- In the folder: `Design_Documents`
2. **Design Flowcharts (for each command)**
- In the folder: `Design_Documents > flowcharts`
3. **Various Manual Testings & Results**
- In the folder: `Testing`
- File name: `TestPlan_ManualTests.xlsx`
4. **A Walkthrough for Usability Testing**
- In the folder: `Testing`
- File name: `Usability_Walkthrough.md`
5. **Usability Survey Results**
- In the folder: `Testing`
- File name: `TaskPaperCLITool_UsabilityTest_Results.xlsx`

---

## 2. TaskPaper CLI Tool Installation via Terminal

**Installation Prerequisites**: `Python version 3.10` or higher

1. Open a Terminal.

2. Navigate to the folder containing the installation (`.whl`) file:

   ```bash
   cd TaskPaper_CLI/dist
   ```
   
3. Install the wheel using either `pipx` (recommended for a standalone CLI application) or `pip`:

   ```bash
   pipx install taskpaper_cli-1.0.0-py3-none-any.whl
   ```

   Or:

   ```bash
   pip install taskpaper_cli-1.0.0-py3-none-any.whl
   ```
   
4. Verify the installed version:

   ```bash
   TaskPaper --version
   ```

   Alternatively:

   ```bash
   TaskPaper -V
   ```

   The expected version is **1.0.0**.

**Note:** The `tabulate` and `termcolor` Python dependencies will be installed automatically when needed by the package installer.

---

## 3. Basic Usage Examples

The following examples illustrate the command-line interface:

```bash
# Display available commands and options
TaskPaper --help

# List projects in the currently opened TaskPaper file
TaskPaper list-projects

# Add a task to a project
TaskPaper add-task --project "Project X" --task "Complete the report"

# Add a tag to a task (the tool prompts you to select the task)
TaskPaper add-tag @priority(high) --project "Project X"

# Mark all tasks matching a tag as done
TaskPaper batch --filter @priority(high) --action mark-done
```

Some commands require a TaskPaper file to be opened first, and interactive commands prompt for additional information.

For command-specific explanations and flowcharts, see the [`Design_Documents`](Design_Documents) folder.

