# Command: `list-projects`
## Description
The `list-projects` command lists all the projects in the currently opened TaskPaper file. Projects are displayed in a numbered list format, showing the total count at the end.

---

## Arguments


### **None** 
This command does not take any arguments.

---

## Design

### Flowchart:

![Flowchart for List-Projects Command](Design_Documents/flowcharts/listProjects.png "List-Projects Command Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to list **all projects** from the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `list projects (multiple projects)`

**CLI input**:
```
python3 main.py list-projects
```
**CLI output**:
```
1. New Project
2. Existing Project
3. Old Project
A total of 3 project(s) listed from file /currently/opened/file.taskpaper.
```
---
#### Example 2: `list projects (single project)`

**CLI input**:
```
python3 main.py list-projects
```
**CLI output**:
```
1. Personal Project
A total of 1 project(s) listed from file /currently/opened/file.taskpaper.
```
---
#### Example 3: `list projects (empty file)`

**CLI input**:
```
python3 main.py list-projects
```
**CLI output**:
```
There are no project in file /currently/opened/file.taskpaper.
```
---
#### Example 4: `with extra CLI arguments`
**CLI input**:
```
python3 main.py list-projects multiple
```
**CLI output**:
```
usage: TaskPaper [-h] {create,open,add-project,list-projects,rename-project} ...
TaskPaper: error: unrecognized arguments: multiple
```
---
