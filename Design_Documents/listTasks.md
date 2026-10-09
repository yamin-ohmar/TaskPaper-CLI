# Command: `list-tasks`
## Description
The `list-tasks` command lists all tasks under a specific project or filter tasks by a specific tag in the currently opened TaskPaper file. 
- If only the **tag** is provided and the **project** is not, the system will list all tasks by a specific tag under all project in the currently opened TaskPaper file. 
- If only the **project** is provided and the **tag** is not, the system will list all the tasks under that specified project.
- When the **tag** is provided to list the tasks, the tasks are printed in a table format with color coding based on their **due dates** and sorted based on their **priority levels**.

This `list-tasks` command with tag filtering is made to be smart as follow (_also case insensitive_):
- `@due`: List all tasks with due date set to them.
- `@today`: List all tasks that due today and all tasks with `@today` tag.
- `@priority`: List all tasks with priority set to them.
- `@priority(high)`: List all tasks with either `@priority(high)` or `@high` tag.
- `@high`: List all tasks with either `@priority(high)` or `@high` tag.
- `@priority(medium)`: List all tasks with either `@priority(medium)` or `@medium` tag.
- `@medium`: List all tasks with either `@priority(medium)` or `@medium` tag.
- `@priority(low)`: List all tasks with either `@priority(low)` or `@low` tag.
- `@low`: List all tasks with either `@priority(low)` or `@low` tag.
- Completed tasks can be filtered using one of these tags:
    - `@done`
    - `@finished`
    - `@completed`

---

## Arguments

### Optional:
(*at lease one of them must be provided*)
- `-p` or `--project`: The name of the project whose tasks will be listed.
- `-t` or `--tag`: The tag to be used to filter the tasks by.

---

## Design

### Flowchart:

When only the **project** is provided:

![Flowchart for List-Tasks Command](Design_Documents/flowcharts/listTasks.png "List-Tasks Command Flowchart")


When the **tag** is provided:

![Flowchart for List-Tasks Command](Design_Documents/flowcharts/listTasks_wTag.png "List-Tasks Command Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **list tasks** under a specific project or by a specific tag in the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage (filter by project only)`

**CLI input**:
```
TaskPaper list-tasks --project "Work Project"
```
**CLI output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.
A total of 3 task(s) listed for project 'Work Project' from file '/currently/opened/file.taskpaper'.
```
---
#### Example 2: `ideal usage (filter by tag only)`

**CLI input**:
```
TaskPaper list-tasks --tag "@done"
```
**CLI output**:
```

=============================================
 Task Color Legend:
    Completed tasks (in green)
    Tasks due within a week (in yellow)
    Overdue tasks (in red)
    Tasks without due dates (default color)
=============================================

=====   ==============  =============================================   ==========
  No.   Project         Task Name                                       Priority
=====   ==============  =============================================   ==========
    1   Personal        Finish the assignment @done @high               high
    2   Work Project    Submit report @low @completed                   low
    3   Personal        Clean the house  @finished
=====   ==============  =============================================   ==========

A total of 3 task(s) listed from file '/currently/opened/file.taskpaper'.
```
---
#### Example 3: `ideal usage (filter by both project and tag)`

**CLI input**:
```
TaskPaper list-tasks --tag "@done" --project "Personal"
```
**CLI output**:
```

=============================================
 Task Color Legend:
    Completed tasks (in green)
    Tasks due within a week (in yellow)
    Overdue tasks (in red)
    Tasks without due dates (default color)
=============================================

=====   ==============  =============================================   ==========
  No.   Project         Task Name                                       Priority
=====   ==============  =============================================   ==========
    1   Personal        Finish the assignment @done @high               high
    2   Personal        Clean the house  @finished
=====   ==============  =============================================   ==========

A total of 2 task(s) listed from file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `project is nonexistent`

**CLI input**:
```
TaskPaper list-tasks --project "Nonexistent Project"
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 5: `tag is nonexistent`

**CLI input**:
```
TaskPaper list-tasks --tag "@nonexistent"
```
**CLI output**:
```
No matching tasks found.
```
---
#### Example 6: `project with no task`

**CLI input**:
```
TaskPaper list-tasks --project "Help Project"
```
**CLI output**:
```
There are no task under project 'Help Project' in file '/currently/opened/file.taskpaper'.
```
---
#### Example 7: `project name is empty`

**CLI input**:
```
TaskPaper list-tasks --project " "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 8: `tag name is empty`

**CLI input**:
```
TaskPaper list-tasks --tag " "
```
**CLI output**:
```
Error: Invalid tag name. The tag name cannot be empty.
```
---
#### Example 9: `missing --project CLI argument`
**CLI input**:
```
TaskPaper list-tasks --project 
```
**CLI output**:
```
usage: TaskPaper list-tasks [-h] [-p PROJECT] [-t TAG]
TaskPaper list-tasks: error: argument -p/--project: expected one argument
```
---
#### Example 10: `missing --tag CLI argument`
**CLI input**:
```
TaskPaper list-tasks --tag 
```
**CLI output**:
```
usage: TaskPaper list-tasks [-h] [-p PROJECT] [-t TAG]
TaskPaper list-tasks: error: argument -t/--tag: expected one argument
```
---
#### Example 11: `no CLI argument`
**CLI input**:
```
TaskPaper list-tasks
```
**CLI output**:
```
Error: Either '--project' or '--tag' must be provided.
```
---
