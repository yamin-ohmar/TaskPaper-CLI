# Command: `list-tags`
## Description
The `list-tags` command lists all the unique tags used in a specific project from the currently opened TaskPaper file. Tags are displayed in a numbered list format, showing the total count at the end.

---

## Arguments


### Required:
- `-p` or `--project`: The name of the project whose tags will be listed.

---

## Design

### Flowchart:

![Flowchart for List-Tagss Command](Design_Documents/flowcharts/listTags.png "List-Tags Command Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---

Attempts to list **all unique tags** from the specified project in the current opened **TaskPaper** file in the following manners:

#### Example 1: `list tags`

**CLI input**:
```
TaskPaper list-tags -p "Work Project"
```
**CLI output**:
```
Unique tags used in project 'Work Project':
1.    @due(2025-04-02)
2.    @priority(high)
3.    @waiting
A total of 3 unique tags used in project 'Work' from file '/currently/opened/file.taskpaper'.
```
---
#### Example 2: `project with no tags`

**CLI input**:
```
TaskPaper list-tags -p "Empty Project"
```
**CLI output**:
```
No tags found in project 'Empty Project'.
```
---
#### Example 3: `project is nonexistent`

**CLI input**:
```
TaskPaper list-tags -p "Nonexistent Project"
```
**CLI output**:
```
Project 'Nonexistent Project' does not exist in file '/currently/opened/file.taskpaper'.
```
---
#### Example 4: `project name is empty`
**CLI input**:
```
TaskPaper list-tags -p " "
```
**CLI output**:
```
Error: Invalid project name. The name cannot be empty.
```
---
#### Example 5: `missing --project CLI argument`
**CLI input**:
```
TaskPaper list-tags -p
```
**CLI output**:
```
usage: TaskPaper list-tags [-h] -p PROJECT
TaskPaper list-tags: error: argument -p/--project: expected one argument
```
---
#### Example 6: `no CLI argument`
**CLI input**:
```
TaskPaper list-tags
```
**CLI output**:
```
usage: TaskPaper list-tags [-h] -p PROJECT
TaskPaper list-tags: error: the following arguments are required: -p/--project
```
---
