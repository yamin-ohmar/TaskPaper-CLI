
# Command: `remove-tag`

## Description

The `remove-tag` command allows users to **interactively remove a tag** from a specific task under a project in the currently opened TaskPaper file. The command lists all tasks in the specified project, then prompts the user to select a task by its index to remove the specified tag from the task's name.

---

## Arguments

### Required:

-   `tag_name`: The tag to be removed from the selected task.
-   `-p` or `--project`: The name of the project where the task is located.

---

## Design

### Flowchart:

![Flowchart for Remove-Tag Command](Design_Documents/flowcharts/removeTag.png "Remove-Tag Command Flowchart")

### Use Cases:

#### Prerequisite:

Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **remove a tag** from a task under a specific project in the currently opened **TaskPaper** file in the following manners:

#### Example 1: `ideal usage`

**CLI input**:
```
TaskPaper remove-tag @important -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task. @important
3. This is an existing task. @today @urgent

Please key in the index of the task to remove the tag from (e.g., 2):
```
**CLI interactive input**:
```
2
```
**CLI output**:
```
Removing tag '@important' from task 'This is an old task. @important' under project 'Work Project' in file '/currently/opened/file.taskpaper'...
Tag successfully removed from task: 'This is an old task.'
```
---
#### Example 2: `project is nonexistent`

**CLI input**:
```
TaskPaper remove-tag @urgent -p "Nonexistent Project"
```
**CLI output**:
```
Error: Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 3: `project with no task`

**CLI input**:
```
TaskPaper remove-tag @urgent -p "Empty Project"
```
**CLI output**:
```
There are no tasks under project 'Empty Project' in file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `tag without '@' symbol`

**CLI input**:
```
TaskPaper remove-tag "today" -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task.
3. This is an existing task. @today @urgent

Please key in the index of the task to remove the tag from (e.g., 2):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
Removing tag '@today' from task 'This is an existing task. @today @urgent' under project 'Work Project' in file '/currently/opened/file.taskpaper'...
Tag successfully removed from task: 'This is an existing task. @urgent'
```
---
#### Example 5: `tag with '@' symbol in middle`

**CLI input**:
```
TaskPaper remove-tag "tod@y" -p "Work Project"
```
**CLI output**:
```
Error: A tag must start with '@' or not contain '@' at all.
```
---
#### Example 6: `empty tag`

**CLI input**:
```
TaskPaper remove-tag "  " -p "Work Project"
```
**CLI output**:
```
Error: Invalid tag. The tag name cannot be empty.
```
---
#### Example 7: `tag name with more than one word`

**CLI input**:
```
TaskPaper remove-tag "finishing up" -p "Work Project"
```
**CLI output**:
```
Error: A tag must be a single word without spaces.
```
---
#### Example 8: `tag not found`

**CLI input**:
```
TaskPaper remove-tag "@today" -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task.
3. This is an existing task. @urgent

Please key in the index of the task to remove the tag from (e.g., 2):
```
**CLI interactive input**:
```
3
```
**CLI output**:
```
The task 'This is an existing task. @urgent' does not contain the tag '@today'.
```
---
#### Example 9: `missing task index`

**CLI input**:
```
TaskPaper remove-tag @urgent -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task.
3. This is an existing task. @urgent

Please key in the index of the task to remove the tag from (e.g., 2):
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
TaskPaper remove-tag @urgent -p "Work Project"
```
**CLI interactive output**:
```
Task(s) in project 'Work Project':
1. This is a new task. @due(2025-03-22)
2. This is an old task.
3. This is an existing task. @urgent

Please key in the index of the task to remove the tag from (e.g., 2):
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
#### Example 11: `missing tag name`

**CLI input**:
```
TaskPaper remove-tag -p "Work Project"
```
**CLI output**:
```
usage: TaskPaper remove-tag [-h] -p PROJECT tag_name
TaskPaper remove-tag: error: the following arguments are required: tag_name
```
---
#### Example 12: `missing project name`

**CLI input**:
```
TaskPaper remove-tag @urgent -p
```
**CLI output**:
```
usage: TaskPaper remove-tag [-h] -p PROJECT tag_name
TaskPaper remove-tag: error: argument -p/--project: expected one argument
```
---
#### Example 13: `missing --project argument`

**CLI input**:
```
TaskPaper remove-tag @urgent
```
**CLI output**:
```
usage: TaskPaper remove-tag [-h] -p PROJECT tag_name
TaskPaper remove-tag: error: the following arguments are required: -p/--project
```
---
