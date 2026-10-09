# Command: `rename-project`
## Description
The `rename-project` command renames an existing project in the currently opened TaskPaper file to a new name. It ensures the original order of projects is preserved and provides warnings or errors for invalid inputs or conflicts.

---

## Arguments


### Required:
- `old_name`: The current name of the project to rename.
- `new_name`: The new name for the project.

---

## Design

### Flowchart:

![Flowchart for Rename-Project Command](Design_Documents/flowcharts/renameProject.png "Rename-Project Command Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **rename project** from the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage`

**CLI input**:
```
python3 main.py rename-project "Old Project" "New Project"
```
**CLI output**:
```
Renaming project 'Old Project' to 'New Project' in file '/currently/opened/file.taskpaper'...
Successfully renamed project 'Old Project' to 'New Project'.
```
---
#### Example 2: `old_name is nonexistent`

**CLI input**:
```
python3 main.py rename-project "Nonexistent Project" "New Project"
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 3: `new_name already exists`

**CLI input**:
```
python3 main.py rename-project "Old Project" "Existing Project"
```
**CLI output**:
```
Project 'Existing Project' already exists in file '/currently/opened/file.taskpaper'. 
Please choose a different name.
```
---
#### Example 4: `old_name is empty`

**CLI input**:
```
python3 main.py rename-project " " "New Project"
```
**CLI output**:
```
Error: Invalid project name(s). The name(s) cannot be empty.
```
---
#### Example 5: `new_name is empty`

**CLI input**:
```
python3 main.py rename-project "Old Project" "  "
```
**CLI output**:
```
Error: Invalid project name(s). The name(s) cannot be empty.
```
---
#### Example 6: `missing one CLI argument`
**CLI input**:
```
python3 main.py rename-project "Old Project"
```
**CLI output**:
```
usage: TaskPaper rename-project [-h] old_name new_name
TaskPaper rename-project: error: the following arguments are required: new_name
```
---
#### Example 7: `missing all CLI arguments`
**CLI input**:
```
python3 main.py rename-project
```
**CLI output**:
```
usage: TaskPaper rename-project [-h] old_name new_name
TaskPaper rename-project: error: the following arguments are required: old_name, new_name
```
---
