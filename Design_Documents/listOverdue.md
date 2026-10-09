# Command: `list-overdue`
## Description
The `list-overdue` command lists all tasks that are past their due date from the currently opened TaskPaper file. If a project is specified, it filters the overdue tasks by that project only. The tasks are sorted and displayed in order of their priority levels.

---

## Arguments

### Optional:
- `-p` or `--project`: The name of the project to filter overdue tasks from. If not specified, tasks from all projects are considered.

---

## Design

### Flowchart:

![Flowchart for List-Overdue Command](Design_Documents/flowcharts/listOverdue.png "List-Overdue Command Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to list **overdue tasks** under a specific project (if specified; if not, list **ALL overdue tasks**) from the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage (all projects)`

**CLI input**:
```
TaskPaper list-overdue
```
**CLI output**:
```

=====   ==============  =============================================   ==========
  No.   Project         Overdue Task(s)                                 Priority
=====   ==============  =============================================   ==========
    1   Personal        Finish the assignment @due(2025-03-07) @high    high
    2   Work Project    Submit report @due(2025-03-25) @low             low
    3   Personal        Clean the house  @due(2024-10-25)
=====   ==============  =============================================   ==========

A total of 3 overdue task(s) listed from file '/currently/opened/file.taskpaper'.
```
---
#### Example 2: `ideal usage (specific project)`

**CLI input**:
```
TaskPaper list-overdue -p "Work Project"
```
**CLI output**:
```

=====   ==============  ====================================    ==========
  No.   Project         Overdue Task(s)                         Priority
=====   ==============  ====================================    ==========
    1   Work Project    Submit report @due(2025-03-25) @low     low
=====   ==============  ====================================    ==========

A total of 1 overdue task(s) listed from file '/currently/opened/file.taskpaper'.
```
---
#### Example 3: `no overdue tasks`

**CLI input**:
```
TaskPaper list-overdue -p "Group Project"
```
**CLI output**:
```
No overdue tasks found.
```
---
#### Example 4: `project is nonexistent`

**CLI input**:
```
TaskPaper list-overdue -p "Nonexistent Project"
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 5: `project name is empty`

**CLI input**:
```
TaskPaper list-overdue -p "  "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 6: `missing --project CLI argument`

**CLI input**:
```
TaskPaper list-overdue -p
```
**CLI output**:
```
usage: TaskPaper list-overdue [-h] [-p PROJECT]
TaskPaper list-overdue: error: argument -p/--project: expected one argument
```
---
