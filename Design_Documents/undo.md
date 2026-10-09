# Command: `undo`
## Description
The `undo` command restores the last state of the TaskPaper file before a certain previous modification; i.e. it works for only one step of undo — the most recent action that modified the TaskPaper file. It restores from the backup file. Once `undo` command is used, the backup file is deleted and the `undo` command cannot be used again until the taskpaper file has been modified again using other commands.

---

## Arguments

### **None** 
This command does not take any arguments.

---

## Design

### Flowchart:

![Flowchart for Undo Command](Design_Documents/flowcharts/undo.png "Undo Command Flowchart")

### Use Cases:

#### Prerequisite:
- Run `open` command before using this command to ensure a TaskPaper file is opened.
- The user must run a command that modifies the TaskPaper file; such as `add-project`, `rename-project`, `delete-project`, `add-task`, `edit-task`, `delete-task`, `move-task`, `add-tag`, `remove-tag`, and `batch` operations before this command can be used.

---

Attempts to **undo** the previous action made to the *currently opened* **TaskPaper** file in the following manners:

#### Example 1: `ideal usage`

**CLI input**:
```
TaskPaper undo
```
**Interactive CLI output**:
```
Are you sure you want to undo the last action ('move-task')? (y/n):
```
**Interactive CLI input**:
```
y
```
**CLI output**:
```
Undo successful: Restored '/currently/opened/file.taskpaper' after 'move-task'.
```
---
#### Example 2: `undo cancelled`

**CLI input**:
```
TaskPaper undo
```
**Interactive CLI output**:
```
Are you sure you want to undo the last action ('move-task')? (y/n):
```
**Interactive CLI input**:
```
n
```
**CLI output**:
```
Undo cancelled.
```
---
#### Example 3: `undo without any recent changes`

**CLI input**:
```
TaskPaper undo
```
**CLI output**:
```
Nothing to undo.
```
---
#### Example 4: `missing backup file`

**CLI input**:
```
TaskPaper undo
```
**Interactive CLI output**:
```
Are you sure you want to undo the last action ('move-task')? (y/n):
```
**Interactive CLI input**:
```
y
```
**CLI output**:
```
The backup file '/currently/opened/file.taskpaper.bak' does not exist.
```
---
