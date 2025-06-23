# Directory Copy Utility

A Python utility for copying directories and files with progress tracking and smart file-skipping capabilities.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- GUI file choosers for selecting source and destination directories
- Recursive copying of files and directories
- Preserves directory structure
- Real-time progress tracking with percentage completion
- Smart file skipping (avoids copying identical files)
- Error handling for permission issues and system files
- Administrator mode for accessing system files

## Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python installation)

## Installation

No installation is required. Simply download the `copy_files.py` script and run it with Python.

```bash
# Clone the repository (if using Git)
git clone https://github.com/yourusername/directory-copy-utility.git

# Or just download the copy_files.py file directly
```

## Usage

### Basic Usage

Run the script using Python:

```bash
python copy_files.py
```

Two file chooser dialogs will appear:
1. First dialog: Select the source directory
2. Second dialog: Select the destination directory

The copying process will begin automatically after both directories are selected.

### Running as Administrator (for copying system files)

To copy system files and folders with restricted permissions, run the script as administrator:

#### Windows

**Method 1: Command Prompt as Admin**
1. Open Command Prompt as Administrator
2. Navigate to the script location
3. Run the script:
   ```
   cd "path\to\script"
   python copy_files.py
   ```

**Method 2: Batch File**
1. Create a batch file with the following content:
   ```batch
   @echo off
   powershell -Command "Start-Process cmd -ArgumentList '/c cd \"path\to\script\" && python copy_files.py && pause' -Verb RunAs"
   ```
2. Save as `run_as_admin.bat` and double-click to run

#### macOS/Linux
```bash
sudo python3 copy_files.py
```

## How It Works

1. **Directory Selection**:
   - The script uses tkinter to create GUI file chooser dialogs
   - User selects source and destination directories

2. **File Counting**:
   - Scans the source directory to count files and directories
   - Displays the total number of items to copy

3. **Permission Check**:
   - Checks if running with administrator privileges
   - Provides appropriate warnings about system file access

4. **Smart Copying Process**:
   - Creates directory structure in the destination
   - For each file:
     - Checks if it already exists in destination with same size and modification time
     - Skips files that are identical (same size and modification time)
     - Copies new or modified files
     - Handles permission errors gracefully

5. **Progress Reporting**:
   - Shows real-time progress updates:
     - Overall completion percentage
     - Files and directories processed
     - Number of files copied vs. skipped
     - Error reporting

6. **Error Handling**:
   - Skips files that cannot be accessed instead of crashing
   - Reports permission issues
   - Continues operation even if some files can't be copied

## Output Example

```
Directory Copying Utility
------------------------------
Note: For copying system files and avoiding permission errors, 
      consider running this script as Administrator.
------------------------------
Select source directory:
Select destination directory:

Copying files from:
Source: C:/Users/Documents
Destination: D:/Backup

Counting files and directories...
Found 1250 files and 85 directories to copy.
--------------------------------------------------
Running without administrator privileges - some system files may be skipped
To copy all system files, run this script as Administrator
--------------------------------------------------
Progress: 25.1% | Directory: 20/85 (23.5%) | Files: 312/1250 (25.0%) | Copied: 312 | Existing: 0 | Errors: 0
Progress: 50.2% | Directory: 42/85 (49.4%) | Files: 625/1250 (50.0%) | Copied: 625 | Existing: 0 | Errors: 0
Progress: 75.3% | Directory: 64/85 (75.3%) | Files: 938/1250 (75.0%) | Copied: 938 | Existing: 0 | Errors: 0
Progress: 100.0% | Directory: 85/85 (100.0%) | Files: 1250/1250 (100.0%) | Copied: 1250 | Existing: 0 | Errors: 0

Copy complete!

Operation completed with no errors!
Files copied: 1250, Files already existed: 0
Directories created: 85
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with Python and tkinter
- Thanks to the Python shutil library for file operations
