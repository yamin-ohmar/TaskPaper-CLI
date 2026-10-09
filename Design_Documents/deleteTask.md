# Command: `delete-task`
## Description
The `delete-task` command allows users to **interactively delete a task** under a specific project in the currently opened TaskPaper file. The command lists all tasks in the specified project, then prompts the user to select a task by its index to delete followed by a confirmation prompt.

---

## Arguments

### Required:
- `-p` or `--project`: The name of the project whose task will be deleted.

---

## Design

### Flowchart:

![Flowchart for Delete-Task Command](Design_Documents/flowcharts/deleteTask.png "Delete-Task Command Flowchart")


### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **delete a task** under a specific project in the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage (confirm)`

**CLI input**:
```
python3 main.py delete-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be deleted (e.g., 2):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
Are you sure you want to delete task: 'This is an existing task.'? (y/n): 
```
**CLI interactive input**:
```
y
```
**CLI output**:
```
Deleting the task 'This is an existing task.' in file '/currently/opened/file.taskpaper'...
Task successfully deleted in project 'Work Project'.
```
---
#### Example 2: `ideal usage (Not confirm)`

**CLI input**:
```
python3 main.py delete-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be deleted (e.g., 2):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
Are you sure you want to delete task: 'This is an existing task.'? (y/n): 
```
**CLI interactive input**:
```
n
```
**CLI output**:
```
Task deletion cancelled.
```
---
#### Example 3: `project is nonexistent`

**CLI input**:
```
python3 main.py delete-task --project "Nonexistent Project"
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `project with no task`

**CLI input**:
```
python3 main.py delete-task --project "Help Project"
```
**CLI output**:
```
There are no task under project 'Help Project' in file '/currently/opened/file.taskpaper'.
```
---
#### Example 5: `project name is empty`

**CLI input**:
```
python3 main.py delete-task --project " "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 6: `missing task index`

**CLI input**:
```
python3 main.py delete-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be deleted (e.g., 2):
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
#### Example 7: `input alphabets for task index`

**CLI input**:

```
python3 main.py delete-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be deleted (e.g., 2):
```
**CLI interactive input**:
```
a
```
**CLI output**:
```
Invalid input. Please enter a number.
```
---
#### Example 8: `invalid task index`

**CLI input**:

```
python3 main.py delete-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be deleted (e.g., 2):
```
**CLI interactive input**:
```
4
```
**CLI output**:
```
Error: Invalid index. Must be from 1 to 3.
```
---
#### Example 9: `missing --project CLI argument`
**CLI input**:
```
python3 main.py delete-task --project 
```
**CLI output**:
```
usage: TaskPaper delete-task [-h] -p PROJECT
TaskPaper delete-task: error: argument -p/--project: expected one argument
```
---
#### Example 10: `no CLI argument`
**CLI input**:
```
python3 main.py delete-task
```
**CLI output**:
```
usage: TaskPaper delete-task [-h] -p PROJECT
TaskPaper delete-task: error: the following arguments are required: -p/--project
```
---
