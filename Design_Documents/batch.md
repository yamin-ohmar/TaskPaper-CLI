# Command: `batch`
## Description
The `batch` command performs bulk operations on tasks filtered by a single tag across all projects in the currently opened TaskPaper file. Currently, it supports operations like marking tasks as done or replacing one tag with another.

---

## Arguments

### Required:
- `-f` or `--filter`: The tag to filter the tasks by.
- `-a` or `--action`: The operation to perform on filtered tasks. Supported actions are as follows:
  - `mark-done`: Add `@done` tag to all the filtered tasks.
  - `replace-tag`: Replace the filtered tag with a new one.

### Optional:
- `-v` or `--value`: To be used only with `replace-tag` action to provide the new tag.

---

## Design

### Flowchart:

![Flowchart for Batch Command](Design_Documents/flowcharts/batch.png "Batch Command Flowchart")

### Use Cases:

#### Prerequisite:
Run `open` command before using this command to ensure a TaskPaper file is opened.

---
#### Example 1: `ideal usage: mark-done`

**CLI input**:
```
TaskPaper batch -f @today -a mark-done
```
**CLI output**:
```
Adding tag '@done' to tasks with tag '@today' in file '/currently/opened/file.taskpaper'...
All matching tasks are now marked as done.
```
---
#### Example 2: `ideal usage: replace-tag`

**CLI input**:
```
TaskPaper batch -f @wait -a replace-tag -v @TBC
```
**CLI output**:
```
Replacing tag '@wait' with '@TBC' in file '/currently/opened/file.taskpaper'...
All matching tags have been replaced with '@TBC'.
```
---
#### Example 3: `missing --value for replace-tag`

**CLI input**:
```
TaskPaper batch -f @wait -a replace-tag
```
**CLI output**:
```
Error: Missing --value for <replace-tag> operation.
```
---
#### Example 5: `missing CLI argument`

**CLI input**:
```
TaskPaper batch -f @wait -a replace-tag -v
```
**CLI output**:
```
usage: TaskPaper batch [-h] -f FILTER -a {mark-done,replace-tag} [-v VALUE]
TaskPaper batch: error: argument -v/--value: expected one argument
```
---
#### Example 5: `mark-done: no matching tasks found`

**CLI input**:
```
TaskPaper batch -f @nonexistent -a mark-done
```
**CLI output**:
```
Either no matching tasks found or they're already marked done.
```
---
#### Example 6: `replace-tag: no matching tasks found`

**CLI input**:
```
TaskPaper batch -f @waiting -a replace-tag -v @TBC
```
**CLI output**:
```
No task with tag '@waiting' found.
```
---
#### Example 7: `unknown action`

**CLI input**:
```
TaskPaper batch -f @today -a shift-duedate
```
**CLI output**:
```
usage: TaskPaper batch [-h] -f FILTER -a {mark-done,replace-tag} [-v VALUE]
TaskPaper batch: error: argument -a/--action: invalid choice: 'shift-duedate' (choose from mark-done, replace-tag)
```
---
