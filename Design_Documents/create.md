# Command: `create`
## Description
The `create` command is for creating a new TaskPaper file in the specified directory. If no directory is specified, the new TaskPaper file will be created in the current working directory.

---

## Arguments

### **Required**:
- `file_name`: The name of the new TaskPaper file to be created. If it doesn’t end with `.taskpaper`, the file extension will be added by the program.
    > if the `file_name` has spaces, place the `file_name` argument in quotation.

### **Optional**:
- `-p` or `--path`: The directory path where the new TaskPaper file will be created. If not provided, the current working directory will be used.
    > if the folder name in directory path has spaces, place the directory path argument in quotation.

---

## Design

### Flowchart:

![Flowchart for Create Command](Design_Documents/flowcharts/create.png "Create Command Flowchart")


### Use Cases:

Attempts to create a new **TaskPaper** file in following manners:

#### Example 1: `in the current directory`

**CLI input**:
```bash
python3 main.py create my_tasks.taskpaper
```
**CLI output**:
```
TaskPaper file '/current/directory/my_tasks.taskpaper' has been created.
```
---
#### Example 2: `in a specified directory`
**CLI input**:
```
python3 main.py create work_tasks.taskpaper -p /Users/yaminohmar/Documents/projects
```
**CLI output**:
```
TaskPaper file '/Users/yaminohmar/Documents/projects/work_tasks.taskpaper' has been created.
```
---
#### Example 3: `file that already exists`
**CLI input**:
```
python3 main.py create existing_file.taskpaper
```
**CLI output**:
```
Error: '/current/directory/existing_file.taskpaper' file already exists.
```
---
#### Example 4: `in a non-accessible directory`
**CLI input**:
```
python3 main.py create work_tasks.taskpaper -p /home/user/projects
```
**CLI output**:
```
Error: Unable to create or access directory '/home/user/projects'. Reason: [Errno 45] Operation not supported: '/home/user'
```
---
#### Example 5: `a file name with no .taskpaper extension`
**CLI input**:
```
python3 main.py create tasks_list
```
**CLI output**:
```
TaskPaper file '/current/directory/tasks_list.taskpaper' has been created.
```
---
#### Example 6: `a file name with invalid characters`
**CLI input**:
```
python3 main.py create "invalid|file*name?.taskpaper"
```
**CLI output**:
```
TaskPaper file '/current/directory/invalid_file_name_.taskpaper' has been created.
```
---
#### Example 7: `with no CLI arguments`
**CLI input**:
```
python main.py create
```
**CLI output**:
```
usage: TaskPaper create [-h] [-p PATH] file_name
TaskPaper create: error: the following arguments are required: file_name
```
---
#### Example 8: `spaces in file_name (no quotation)`
**CLI input**:
```
python3 main.py create hello world.taskpaper
```
**CLI output**:
```
usage: TaskPaper [-h] {create,open,add-project,list-projects,rename-project} ...
TaskPaper: error: unrecognized arguments: world.taskpaper
```
---
#### Example 9: `spaces in file_name (with quotation)`
**CLI input**:
```
python3 main.py create "hello world.taskpaper"
```
**CLI output**:
```
TaskPaper file '/current/directory/hello world.taskpaper' has been created.
```
---
#### Example 10: `spaces in --path (no quotation)`
**CLI input**:
```
python3 main.py create work_tasks.taskpaper -p /Users/yaminohmar/Documents/Monday Project
```
**CLI output**:
```
usage: TaskPaper [-h] {create,open,add-project,list-projects,rename-project} ...
TaskPaper: error: unrecognized arguments: Project
```
---
#### Example 11: `spaces in --path (with quotation)`
**CLI input**:
```
python3 main.py create work_tasks.taskpaper -p "/Users/yaminohmar/Documents/Monday Project"
```
**CLI output**:
```
TaskPaper file '/Users/yaminohmar/Documents/Monday Project/work_tasks.taskpaper' has been created.
```
---
