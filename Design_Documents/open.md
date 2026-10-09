# Command: `open`
## Description
The `open` command is used to open a specified TaskPaper file. The file path is then stored in memory (via a temporary file) for subsequent commands to use for reading the file and fetching/manipulating the data.

---

## Arguments

### **Required**:
- `file_path`: The absolute or relative path to the TaskPaper file to open.
    > if the folder name in `file_path` has spaces, place the `file_path` argument in quotation.

---

## Design

### Flowchart:

![Flowchart for Open Command](Design_Documents/flowcharts/open.png "Open Command Flowchart")


### Use Cases:

Attempts to open a **TaskPaper** file in following manners:

#### Example 1: `a valid file (no path)`

**CLI input**:
```
python3 main.py open my_tasks.taskpaper
```
**CLI output**:
```
Successfully loaded filepath '/current/working/my_tasks.taskpaper' into memory.
```
---
#### Example 2: `a valid file (absolute path)`

**CLI input**:
```
python3 main.py open /Users/yaminohmar/Documents/projects/work_tasks.taskpaper
```
**CLI output**:
```
Successfully loaded filepath '/Users/yaminohmar/Documents/projects/work_tasks.taskpaper' into memory.
```
---
#### Example 3: `a valid file (relational path)`

**CLI input**:
```
python3 main.py open ../task_lists.taskpaper
```
**CLI output**:
```
Successfully loaded filepath '/absolute/path/to/task_lists.taskpaper' into memory.
```
---
#### Example 4:  `non-accessible directory`
**CLI input**:
```
python3 main.py open /home/user/projects/work_tasks.taskpaper
```
**CLI output**:
```
Error: File '/home/user/projects/work_tasks.taskpaper' does not exist or is not accessible.
```
---
#### Example 5: `a file name without .taskpaper extension`
**CLI input**:
```
python3 main.py open my_tasks
```
**CLI output**:
```
Please provide the full file name including the file name extension.
```
---
#### Example 6: `just directory (no file name)`
**CLI input**:
```
python3 main.py open /Users/yaminohmar/Documents/projects/
```
**CLI output**:
```
Please provide the full file name including the file name extension.
```
---
#### Example 7: `without CLI arguments`
**CLI input**:
```
python3 main.py open
```
**CLI output**:
```
usage: TaskPaper open [-h] file_path
TaskPaper open: error: the following arguments are required: file_path
```
---
#### Example 8: `spaces in file_path (no quotation)`
**CLI input**:
```
python3 main.py open /Users/yaminohmar/Documents/Monday Project/tasks.taskpaper
```
**CLI output**:
```
usage: TaskPaper [-h] {create,open,add-project,list-projects,rename-project} ...
TaskPaper: error: unrecognized arguments: Project/tasks.taskpaper
```
---
#### Example 9: `spaces in file_path (with quotation)`
**CLI input**:
```
python3 main.py open "/Users/yaminohmar/Documents/Monday Project/tasks.taskpaper"
```
**CLI output**:
```
Successfully loaded filepath '/Users/yaminohmar/Documents/Monday Projects/tasks.taskpaper' into memory.
```
---
