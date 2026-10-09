
# Command: `add-tag`

## Description

The `add-tag` command allows users to **interactively add a tag** to a specific task under a project in the currently opened TaskPaper file. The command lists all tasks in the specified project, then prompts the user to select a task by its index and adds the specified tag to the task's name.

---

## Arguments

### Required:

-   `tag_name`: The tag to be added to the selected task.
-   `-p` or `--project`: The name of the project where the task is located.

---

## Design

### Flowchart:

![Flowchart for Add-Tag Command](Design_Documents/flowcharts/addTag.png "Add-Tag Command Flowchart")

### Use Cases:

#### Prerequisite:

Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **add a tag** to a task under a specific project in the currently opened **TaskPaper** file in the following manners:

#### Example 1: `ideal usage`

**CLI input**:
```
TaskPaper add-tag @important -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task.
2. This is an old task.
3. This is an existing task.

Please key in the index of the task for tag to be added (e.g., 2):
```
**CLI interactive input**:
```
2
```
**CLI output**:
```
Adding tag '@important' to task 'This is an old task.' under project 'Work Project' in file '/currently/opened/file.taskpaper'...
Tag successfully added to task: 'This is an old task. @important'
```
---
#### Example 2: `project is nonexistent`

**CLI input**:
```
TaskPaper add-tag @urgent -p "Nonexistent Project"
```
**CLI output**:
```
Error: Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 3: `project with no task`

**CLI input**:
```
TaskPaper add-tag @urgent -p "Empty Project"
```
**CLI output**:
```
There are no tasks under project 'Empty Project' in file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `tag without '@' symbol`

**CLI input**:
```
TaskPaper add-tag "today" -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task.
2. This is an old task. @important
3. This is an existing task.

Please key in the index of the task for tag to be added (e.g., 2):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
Adding tag '@today' to task 'This is an existing task.' under project 'Work Project' in file '/currently/opened/file.taskpaper'...
Tag successfully added to task: 'This is an existing task. @today'
```
---
#### Example 5: `tag with '@' symbol in middle`

**CLI input**:
```
TaskPaper add-tag "tod@y" -p "Work Project"
```
**CLI output**:
```
Error: A tag must start with '@' or not contain '@' at all.
```
---
#### Example 6: `empty tag`

**CLI input**:
```
TaskPaper add-tag "  " -p "Work Project"
```
**CLI output**:
```
Error: Invalid tag. The tag name cannot be empty.
```
---
#### Example 7: `tag name with more than one word`

**CLI input**:
```
TaskPaper add-tag "finishing up" -p "Work Project"
```
**CLI output**:
```
Error: A tag must be a single word without spaces.
```
---
#### Example 8: `correct due date tag format`

**CLI input**:
```
TaskPaper add-tag "@due(2025-03-22)" -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task.
2. This is an old task. @important
3. This is an existing task. @today

Please key in the index of the task for tag to be added (e.g., 2):
```
**CLI interactive input**:
```
1
```
**CLI output**:
```
Adding tag '@due(2025-03-22)' to task 'This is a new task.' under project 'Work Project' in file '/currently/opened/file.taskpaper'...
Tag successfully added to task: 'This is a new task. @due(2025-03-22)'
```
---
#### Example 9: `incorrect due date tag format`

**CLI input**:
```
TaskPaper add-tag "@due(25-03-22)" -p "Work Project"
```
**CLI output**:
```
Error: Invalid due date format. Please use '@due(YYYY-MM-DD)'.
```
---
#### Example 10: `due date tag without date`

**CLI input**:
```
TaskPaper add-tag "@due" -p "Work Project"
```
**CLI output**:
```
Error: Invalid due date format. Please use '@due(YYYY-MM-DD)'.
```
---
#### Example 11: `duplicate tag`

**CLI input**:
```
TaskPaper add-tag "@today" -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task. @important
3. This is an existing task. @today

Please key in the index of the task for tag to be added (e.g., 2):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
Task 'This is an existing task. @today' already has the tag '@today'.
```
---
#### Example 12: `multiple tags`

**CLI input**:
```
TaskPaper add-tag "@urgent" -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task. @important
3. This is an existing task. @today

Please key in the index of the task for tag to be added (e.g., 2):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
Adding tag '@urgent' to task 'This is an existing task. @today' under project 'Work Project' in file '/currently/opened/file.taskpaper'...
Tag successfully added to task: 'This is an existing task. @today @urgent'
```
---
#### Example 13: `missing task index`

**CLI input**:
```
TaskPaper add-tag @urgent -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task. @important
3. This is an existing task. @today @urgent

Please key in the index of the task to add the tag to (e.g., 2):
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
#### Example 14: `invalid task index`

**CLI input**:
```
TaskPaper add-tag @urgent -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task. @important
3. This is an existing task. @today @urgent

Please key in the index of the task to add the tag to (e.g., 2):
```
**CLI interactive input**:
```
5
```
**CLI output**:
```
Error: Invalid index. Must be from 1 to 3.
```
---
#### Example 15: `missing tag name`

**CLI input**:
```
TaskPaper add-tag -p "Work Project"
```
**CLI output**:
```
usage: TaskPaper add-tag [-h] -p PROJECT tag_name
TaskPaper add-tag: error: the following arguments are required: tag_name
```
---
#### Example 16: `missing project name`

**CLI input**:
```
TaskPaper add-tag @urgent -p
```
**CLI output**:
```
usage: TaskPaper add-tag [-h] -p PROJECT tag_name
TaskPaper add-tag: error: argument -p/--project: expected one argument
```
---
#### Example 17: `missing --project argument`

**CLI input**:
```
TaskPaper add-tag @urgent
```
**CLI output**:
```
usage: TaskPaper add-tag [-h] -p PROJECT tag_name
TaskPaper add-tag: error: the following arguments are required: -p/--project
```
---
