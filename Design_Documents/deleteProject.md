# Command: `delete-project`
## Description
The `delete-project` command allows users to **delete a project** and all its tasks (*if any*) in the currently opened TaskPaper file. It prompts the user to confirm the deletion of the entire project before it actually deletes it.

---

## Arguments

### Required:
- `project_name`: The name of the project to be deleted from the currently opened TaskPaper file.

    > if the `project_name` argument has spaces, place the `project_name` argument in quotation.

---

## Design

### Flowchart:

![Flowchart for Delete-Project Command](Design_Documents/flowcharts/deleteProject.png "Delete-Project Command Flowchart")


### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to **delete a project** and its tasks (*if any*) from the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage (confirm)`

**CLI input**:
```
python3 main.py delete-project "Work Project"
```
**CLI output**:
```
Are you sure you want to delete the entire project: 'Work Project'? (y/n): 
```
**CLI input**:
```
y
```
**CLI output**:
```
Deleting the project 'Work Project' in file '/currently/opened/file.taskpaper'...
Successfully deleted the project 'Work Project'.
```
---
#### Example 2: `ideal usage (Not confirm)`

**CLI input**:

```
python3 main.py delete-project "Work Project"
```
**CLI output**:
```
Are you sure you want to delete the entire project: 'Work Project'? (y/n): 
```
**CLI input**:
```
n
```
**CLI output**:
```
Project deletion cancelled.
```
---
#### Example 3: `project is nonexistent`

**CLI input**:
```
python3 main.py delete-project "Nonexistent Project"
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `project name is empty`

**CLI input**:
```
python3 main.py delete-project " "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 5: `no CLI argument`
**CLI input**:
```
python3 main.py delete-task
```
**CLI output**:
```
usage: TaskPaper delete-project [-h] project_name
TaskPaper delete-project: error: the following arguments are required: project_name
```
---
