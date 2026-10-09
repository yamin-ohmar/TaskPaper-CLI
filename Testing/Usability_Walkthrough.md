# TaskPaper CLI Tool

## Usability Test Instructions - A Walkthrough

**Objective**: Observe how easily a user can complete common tasks using the TaskPaper CLI tool, and evaluate the system design based on established usability principles through Heuristic Evaluation.

## Instructions for Users
Please complete the following steps using the TaskPaper CLI tool. Let me know if anything is confusing or doesn't work as expected.

1.  **Create a new TaskPaper file**
```
TaskPaper create test.taskpaper
```

2.  **Open the file**
```
TaskPaper open test.taskpaper
```

3.  **Add a project**
```
TaskPaper add-project Personal
```

4.  **Add a task to the project**
```
TaskPaper add-task --project "Personal" --task "Buy groceries @due(2025-05-10) @priority(medium)"
```  

5.  **Add another task under same project**
```
TaskPaper add-task --project "Personal" --task "Clean house @due(2025-05-01) @low"
```

6.  **List tasks using a tag for all tasks with due date**
```
TaskPaper list-tasks --tag "@due"
```

7.  **Add tag using interactive input**
```
TaskPaper add-tag "@urgent" --project "Personal"
Interactive input: 1
```

8.  **List tasks under a project**
```
TaskPaper list-tasks --project "Personal"
```

9.  **Run a batch command**
```
TaskPaper batch --filter @urgent --action mark-done
```

10.  **Delete a task under a project interactively**
```
TaskPaper delete-task --project "Personal"
Interactive input: 2
```

11.  **Try asking for help by typing "help"**
```
TaskPaper help
TaskPaper -h
```

12.  **Try mistyping a command**
```
TaskPaper crate
```

13.  **Undo the last operation**
```
TaskPaper undo
```

14.  **List tasks using a tag for all tasks with priority**
```
TaskPaper list-tasks --tag "@priority"
```

15.  **Check the version of the tool**
```
TaskPaper -V
```
