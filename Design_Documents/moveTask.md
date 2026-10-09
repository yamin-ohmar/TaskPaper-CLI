
# Command: `move-task`

## Description

The `move-task` command allows users to **interactively move a task** from a specific project to another project in the currently opened TaskPaper file. The command lists all tasks in the specified project, then prompts the user to select a task by its index to move it to another project.

---

## Arguments

### Required:

- `--from`: The name of the project where task is currently in.
- `--to`: The name of the project where task is to be moved to.

---

## Design

### Flowchart:

![Flowchart for Move-Task Command](Design_Documents/flowcharts/moveTask.png "Move-Task Command Flowchart")

### Use Cases:

#### Prerequisite:

Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **move a task** from a specific project to another project in the currently opened **TaskPaper** file in the following manners:

#### Example 1: `task moving (confirm)`

**CLI input**:
```
TaskPaper move-task --from "Work Project" --to "Home Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task. @important
3. This is an existing task. @today @urgent

Please key in the index of the task to be moved (e.g., 2):
```
**CLI interactive input**:
```
2
```
**CLI interactive output**:
```
Are you sure you want to move task 'This is an old task. @important' and its sub-tasks (if any) to project 'Home Project'? (y/n):
```
**CLI interactive input**:
```
y
```
**CLI output**:
```
Moving the task 'This is an old task. @important' and its sub-tasks (if any) to project 'Home Project' in file '/currently/opened/file.taskpaper'...
Task successfully moved from project 'Work Project' to project 'Home Project'.
```
---
#### Example 2: `task moving (not confirm)`

**CLI input**:
```
TaskPaper move-task --from "Work Project" --to "Home Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an existing task. @today @urgent

Please key in the index of the task to be moved (e.g., 2):
```
**CLI interactive input**:
```
1
```
**CLI interactive output**:
```
Are you sure you want to move task 'yes @loW' and its sub-tasks (if any) to project 'Home Project'? (y/n):
```
**CLI interactive input**:
```
y
```
**CLI output**:
```
Task moving cancelled.
```
---
#### Example 3: `to nonexisting project`

**CLI input**:
```
TaskPaper move-task --from "Work Project" --to "Nonexistent Project"
```
**CLI output**:
```
Error: Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `from nonexisting project`

**CLI input**:
```
TaskPaper move-task --from "Nonexistent Project" --to "Home Project"
```
**CLI output**:
```
Error: Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 5: `from project with no task`

**CLI input**:
```
TaskPaper move-task --from "Empty Project" --to "Home Project"
```
**CLI output**:
```
There are no tasks under project 'Empty Project' in file '/currently/opened/file.taskpaper'.
```
---
#### Example 6: `to project with no name`

**CLI input**:
```
TaskPaper move-task --from "Work Project" --to "  "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 7: `from project with no name`

**CLI input**:
```
TaskPaper move-task --from "  " --to "Home Project"
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 8: `same project names`

**CLI input**:
```
TaskPaper move-task --from "Home Project" --to "Home Project"
```
**CLI output**:
```
Source project name and destination project name are the same. No changes made.
```
---
#### Example 9: `missing task index`

**CLI input**:

```
TaskPaper move-task --from "Work Project" --to "Home Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an existing task. @today @urgent

Please key in the index of the task to be moved (e.g., 2):
```
**CLI interactive input**:
```
<no_input>
```
**CLI output**:
```
Invalid input. Please enter a number.
```
---
#### Example 10: `invalid task index`

**CLI input**:

```
TaskPaper move-task --from "Work Project" --to "Home Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an existing task. @today @urgent

Please key in the index of the task to be moved (e.g., 2):
```
**CLI interactive input**:
```
5
```
**CLI output**:
```
Error: Invalid index. Must be from 1 to 2.
```
---
#### Example 11: `missing destination project name`

**CLI input**:
```
TaskPaper move-task --from "Work Project" --to
```
**CLI output**:
```
usage: TaskPaper move-task [-h] --from FROM --to TO
TaskPaper move-task: error: argument --to: expected one argument
```
---
#### Example 12: `missing source project name`

**CLI input**:
```
TaskPaper move-task --from --to "Home Project"
```
**CLI output**:
```
usage: TaskPaper move-task [-h] --from FROM --to TO
TaskPaper move-task: error: argument --from: expected one argument
```
---
#### Example 13: `missing --to argument`

**CLI input**:
```
TaskPaper move-task --from "Work Project"
```
**CLI output**:
```
usage: TaskPaper move-task [-h] --from FROM --to TO
TaskPaper move-task: error: the following arguments are required: --to
```
---
#### Example 14: `missing --from argument`

**CLI input**:
```
TaskPaper move-task --to "Home Project"
```
**CLI output**:
```
usage: TaskPaper move-task [-h] --from FROM --to TO
TaskPaper move-task: error: the following arguments are required: --from
```
---
#### Example 15: `missing all CLI arguments`

**CLI input**:
```
TaskPaper move-task
```
**CLI output**:
```
usage: TaskPaper move-task [-h] --from FROM --to TO
TaskPaper move-task: error: the following arguments are required: --from, --to
```
---
