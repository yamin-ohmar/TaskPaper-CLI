# Command: `add-task`
## Description
The `add-task` command adds a new task to a specific project in the currently opened TaskPaper file. If the specified project does not exist or the task is a duplicate, an error message is displayed.

---

## Arguments


### Required:
- `-p` or `--project`: The name of the project to which the task will be added.
- `-t` or `--task`: The description of the task to add.

---

## Design

### Flowchart:

![Flowchart for Add-Task Command](Design_Documents/flowcharts/addTask.png "Add-Task Command Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **add a task** to an existing project in the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage`

**CLI input**:
```
python3 main.py add-task --project "Work Project" --task "This is a new task."
```
**CLI output**:
```
Adding task 'This is a new task.' to project 'Work Project' in file '/currently/opened/file.taskpaper'...
Added task 'This is a new task.' successfully.
```
---
#### Example 2: `project is nonexistent`

**CLI input**:
```
python3 main.py add-task --project "Nonexistent Project" --task "This is a new task."
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 3: `task already exists under the given project`

**CLI input**:
```
python3 main.py add-task --project "Work Project" --task "This is an existing task."
```
**CLI output**:
```
Task 'This is an existing task.' already exists in project 'hello'.
```
---
#### Example 4: `project name is empty`

**CLI input**:
```
python3 main.py add-task --project " " --task "This is a new task."
```
**CLI output**:
```
Error: Invalid project name (or) task name. The name(s) cannot be empty.
```
---
#### Example 5: `task name is empty`

**CLI input**:
```
python3 main.py add-task --project "Work Project" --task "  "
```
**CLI output**:
```
Error: Invalid project name (or) task name. The name(s) cannot be empty.
```
---
#### Example 6: `missing --project CLI argument`
**CLI input**:
```
python3 main.py add-task --project --task "This is a new task."
```
**CLI output**:
```
usage: TaskPaper add-task [-h] -p PROJECT -t TASK
TaskPaper add-task: error: argument -p/--project: expected one argument
```
---
#### Example 7: `missing --task CLI argument`
**CLI input**:
```
python3 main.py add-task --project "Work Project" --task
```
**CLI output**:
```
usage: TaskPaper add-task [-h] -p PROJECT -t TASK
TaskPaper add-task: error: argument -t/--task: expected one argument
```
#### Example 8: `missing all CLI arguments`
**CLI input**:
```
python3 main.py add-task
```
**CLI output**:
```
usage: TaskPaper add-task [-h] -p PROJECT -t TASK
TaskPaper add-task: error: the following arguments are required: -p/--project, -t/--task
```
---
