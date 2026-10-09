# Command: `edit-task`
## Description
The `edit-task` command allows users to **interactively edit a task** under a specific project in the currently opened TaskPaper file. The command lists all tasks in the specified project, then prompts the user to select a task by its index and to provide the updated text.

---

## Arguments

### Required:
- `-p` or `--project`: The name of the project whose task will be edited.

---

## Design

### Flowchart:

![Flowchart for Edit-Task Command](Design_Documents/flowcharts/editTask.png "Edit-Task Command Flowchart")


### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **edit a task** under a specific project in the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage`

**CLI input**:
```
python3 main.py edit-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be edited and the updated text for that task (e.g., 2 "Updated Task Text"):
```
**CLI interactive input**:
```
3 "This is an on-going task."
```
**CLI output**:
```
Updating the task 'This is an existing task.' to 'This is an on-going task.' in file '/currently/opened/file.taskpaper'...
Task successfully updated in project 'Work Project'.
```
---
#### Example 2: `project is nonexistent`

**CLI input**:
```
python3 main.py edit-task --project "Nonexistent Project"
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 3: `project with no task`

**CLI input**:
```
python3 main.py edit-task --project "Help Project"
```
**CLI output**:
```
There are no task under project 'Help Project' in file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `project name is empty`

**CLI input**:
```
python3 main.py edit-task --project " "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 5: `missing task index`

**CLI input**:
```
python3 main.py edit-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be edited and the updated text for that task (e.g., 2 "Updated Task Text"):
```
**CLI interactive input**:
```
"This is an on-going task."
```
**CLI output**:
```
Invalid input. Format should be: <index> "<updated text>"
```
---
#### Example 6: `missing updated text`

**CLI input**:
```
python3 main.py edit-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be edited and the updated text for that task (e.g., 2 "Updated Task Text"):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
Invalid input. Format should be: <index> "<updated text>"
```
---
#### Example 7: `invalid task index`

**CLI input**:
```
python3 main.py edit-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be edited and the updated text for that task (e.g., 2 "Updated Task Text"):
```
**CLI interactive input**:
```
4 "This is an on-going task."
```
**CLI output**:
```
Error: Invalid index. Must be from 1 to 3.
```
---
#### Example 8: `empty updated text`

**CLI input**:
```
python3 main.py edit-task --project "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
 1. This is a new task.
 2. This is an old task.
 3. This is an existing task.

Please key in the index of the task to be edited and the updated text for that task (e.g., 2 "Updated Task Text"):
```
**CLI interactive input**:
```
3 "   "
```
**CLI output**:
```
Error: Invalid updated text. The new task name cannot be empty.
```
---
#### Example 9: `missing --project CLI argument`
**CLI input**:
```
python3 main.py edit-task --project 
```
**CLI output**:
```
usage: TaskPaper edit-task [-h] -p PROJECT
TaskPaper edit-task: error: argument -p/--project: expected one argument
```
---
#### Example 10: `no CLI argument`
**CLI input**:
```
python3 main.py edit-task
```
**CLI output**:
```
usage: TaskPaper edit-task [-h] -p PROJECT
TaskPaper edit-task: error: the following arguments are required: -p/--project
```
---
