# Command: `add-project`
## Description
The `add-project` command adds a new project to the currently opened TaskPaper file. If a project with the same name already exists, the system will warn the user and will not be making the changes.

---

## Arguments

### **Required**:
- `project_name`: The name of the project to add to the currently opened TaskPaper file.
    > if the `project_name` argument has spaces, place the `project_name` argument in quotation.

---

## Design

### Flowchart:

![Flowchart for Add-Project Command](Design_Documents/flowcharts/addProject.png "Add-Project Command Flowchart")

**Process for Parsing TaskPaper Data:**

![Flowchart for Parsing TaskPaper Data](Design_Documents/flowcharts/parseTaskpaperData.png "Parsing TaskPaper Data Flowchart")

**Process for Serialising TaskPaper Data:**

![Flowchart for Serialising TaskPaper Data](Design_Documents/flowcharts/serializeTaskpaperData.png "Serialising TaskPaper Data Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to add a **new project** to the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `new project`

**CLI input**:
```
python3 main.py add-project work
```
**CLI output**:
```
Added project 'work' successfully.
```
---
#### Example 2: `duplicate project`

**CLI input**:
```
python3 main.py add-project duplicate
```
**CLI output**:
```
Project 'duplicate' already exists.
```
---
#### Example 3: `when no file is opened yet`

**CLI input**:
```
python3 main.py add-project planning
```
**CLI output**:
```
No TaskPaper file is currently opened. Use the 'open' command first.
```
---
#### Example 4:  `when opened file is not accessible`
**CLI input**:
```
python3 main.py add-project allocations
```
**CLI output**:
```
The file '/currently/opened/file.taskpaper' does not exist. Please use the 'open' command first.
```
---
#### Example 5: `without CLI arguments`
**CLI input**:
```
python3 main.py add-project
```
**CLI output**:
```
usage: TaskPaper add-project [-h] project_name
TaskPaper add-project: error: the following arguments are required: project_name
```
---
#### Example 6: `spaces in project_name (no quotation)`
**CLI input**:
```
python3 main.py add-project new project
```
**CLI output**:
```
usage: TaskPaper [-h] {create,open,add-project,list-projects,rename-project} ...
TaskPaper: error: unrecognized arguments: project
```
---
#### Example 7: `spaces in project_name (with quotation)`
**CLI input**:
```
python3 main.py add-project "new project"
```
**CLI output**:
```
Added project 'new project' successfully.
```
---
#### Example 8: `empty project_name`
**CLI input**:
```
python3 main.py add-project " "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
