# TaskPaper Command-Line Interface (CLI)

 > By Yamin Ohmar

## 1. Contents in this repository

### 1.1. TaskPaper CLI Tool (Code related items)
1. **Source Code** 
- In the folder: `TaskPaper_CLI > src`
2. **Installation Files (Distribution Files)**
- In the folder: `TaskPaper_CLI > dist`
- Latest release: `taskpaper_cli-1.0.0-py3-none-any.whl`
3. **Automated Testing Scripts (Unit Testing Files)**
- In the folder: `TaskPaper_CLI > tests`


### 1.2. Documentations
1. **Design Documents (for each command)**
- In the folder: `Design_Documents`
2. **Design Flowcharts (for each command)**
- In the folder: `Design_Documents > flowcharts`
3. **Various Manual Testings & Results**
- In the folder: `Testing`
- File name: `TestPlan_ManualTests.xlsx`
4. **A Walkthrough for Usability Testing**
- In the folder: `Testing`
- File name: `Usability_Walkthrough.md`
5. **Usability Survey Results**
- In the folder: `Testing`
- File name: `TaskPaperCLITool_UsabilityTest_Results.xlsx`

***

## 2. TaskPaper CLI Tool Installation via Terminal

**Installation Prerequisites**: `Python version 3.10` or higher

1. Open a Terminal.
2. Use the **change directory** command (`cd`) to go to the folder where the installation (`.whl`) file exists.
3. Use `pip install xxx.whl` or `pipx install xxx.whl` to install.
    > (replace `xxx` with the name of `.whl` file).
4. Use `TaskPaper --version` or `TaskPaper -V` to check if it is installed Version 1.0.0.

**Note**: `tabulate` and `termcolor` **Python's libraries/modules** will be installed if user doesn't have them in their environment yet.


