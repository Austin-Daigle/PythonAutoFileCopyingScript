# Automated Python Directory Copying
This is a Python utility that copies directories and their contents with real-time progress tracking, error handling, and smart file skipping.  

## How to use:
Download the [source code](copy_files.py) and run it with Python:

```
python copy_files.py
```

When the program starts, you'll be prompted to select a source directory and destination directory via file choosers. The program will copy all files from the source to the destination, preserving the directory structure.

![File Copy Progress](https://user-images.githubusercontent.com/100094056/193491127-90dc68c2-61db-408e-bb0a-23c7e518e65c.PNG)

### Running as Administrator
To copy system files that require special permissions, run as administrator:

1. Right-click on Command Prompt and select "Run as administrator"
2. Navigate to the script directory and run it:
   ```
   cd "C:\Users\Austin\Georgia Tech Dev"
   python copy_files.py
   ```

## Features:
* Preserves directory structure during copying
* Shows real-time progress with percentages
* Skips files that already exist with the same size and modification time
* Handles permission errors gracefully
* Works with system files when run as administrator

## Technical Details
The script uses these key functions:

* `select_directory(title)`: Opens file chooser dialogs
* `is_admin()`: Checks for administrator privileges
* `count_items(directory)`: Counts files and directories recursively
* `copy_directory_contents(source_dir, dest_dir)`: Performs the copying with error handling

The program intelligently compares existing files by both size and modification time, making it efficient for repeated backups.
