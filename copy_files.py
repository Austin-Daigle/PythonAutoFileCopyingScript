import os
import shutil
import tkinter as tk
from tkinter import filedialog
import time
import ctypes
import sys
import stat

def select_directory(title):
    """
    Opens a directory chooser dialog with the specified title.
    Returns the selected directory path.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory = filedialog.askdirectory(title=title)
    return directory

def is_admin():
    """
    Check if the script is running with administrator privileges
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def count_items(directory):
    """
    Count the total number of files and directories in a directory (recursively)
    """
    total_files = 0
    total_dirs = 0
    
    for root, dirs, files in os.walk(directory, onerror=lambda err: None):
        total_files += len(files)
        total_dirs += len(dirs)
    
    return total_files, total_dirs

def copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copies all files and directories from source_dir to dest_dir.
    Shows progress updates during the copy process.
    Handles permission errors gracefully.
    """
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # First count total files and directories
    print("Counting files and directories...")
    total_files, total_dirs = count_items(source_dir)
    print(f"Found {total_files} files and {total_dirs} directories to copy.")
    print("-" * 50)
    
    # Check if admin rights are available
    if is_admin():
        print("Running with administrator privileges - can access system files")
    else:
        print("Running without administrator privileges - some system files may be skipped")
        print("To copy all system files, run this script as Administrator")
    print("-" * 50)
    
    # Count for reporting
    files_copied = 0
    dirs_created = 0
    files_skipped = 0
    dirs_skipped = 0
    last_update_time = time.time()
    errors = []
    
    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir, onerror=lambda err: errors.append(str(err))):
        # Calculate the relative path to maintain directory structure
        try:
            rel_path = os.path.relpath(root, source_dir)
            
            # Create corresponding subdirectory in destination
            if rel_path != '.':
                dest_subdir = os.path.join(dest_dir, rel_path)
                try:
                    if not os.path.exists(dest_subdir):
                        os.makedirs(dest_subdir)
                        dirs_created += 1
                except (PermissionError, OSError) as e:
                    dirs_skipped += 1
                    errors.append(f"Cannot create directory {dest_subdir}: {str(e)}")
                    continue
                
                # Show progress update for directories (not too frequently)
                current_time = time.time()
                if dirs_created == 1 or dirs_created == total_dirs or current_time - last_update_time >= 0.5:
                    dir_percent = (dirs_created / total_dirs * 100) if total_dirs > 0 else 100
                    overall_percent = ((dirs_created + files_copied) / (total_dirs + total_files) * 100) 
                    print(f"Progress: {overall_percent:.1f}% | Directory: {dirs_created}/{total_dirs} ({dir_percent:.1f}%) | "
                          f"Files: {files_copied}/{total_files} ({(files_copied / total_files * 100) if total_files > 0 else 100:.1f}%) | Skipped: {dirs_skipped + files_skipped}")
                    last_update_time = current_time
            
            # Copy all files in the current directory
            for file in files:
                source_file = os.path.join(root, file)
                if rel_path == '.':
                    dest_file = os.path.join(dest_dir, file)
                else:
                    dest_file = os.path.join(dest_dir, rel_path, file)
                
                # Try to copy the file using different methods based on file attributes
                try:
                    # Try to make the source file temporarily more accessible
                    if os.path.exists(source_file):
                        try:
                            # Get current permissions
                            current_mode = os.stat(source_file).st_mode
                            # Add read permission
                            os.chmod(source_file, current_mode | stat.S_IRUSR)
                        except (PermissionError, OSError):
                            pass  # Couldn't change permissions, continue anyway
                    
                    # Copy the file
                    shutil.copy2(source_file, dest_file)
                    files_copied += 1
                except (PermissionError, OSError, shutil.Error) as e:
                    files_skipped += 1
                    errors.append(f"Cannot copy {source_file}: {str(e)}")
                    continue
                
                # Show progress update for files (not too frequently)
                current_time = time.time()
                if files_copied == 1 or files_copied == total_files or current_time - last_update_time >= 0.5:
                    file_percent = (files_copied / total_files * 100) if total_files > 0 else 100
                    overall_percent = ((dirs_created + files_copied) / (total_dirs + total_files) * 100) 
                    print(f"Progress: {overall_percent:.1f}% | Directory: {dirs_created}/{total_dirs} ({(dirs_created / total_dirs * 100) if total_dirs > 0 else 100:.1f}%) | "
                          f"Files: {files_copied}/{total_files} ({file_percent:.1f}%) | Skipped: {dirs_skipped + files_skipped}")
                    last_update_time = current_time
        except Exception as e:
            errors.append(f"Error processing {root}: {str(e)}")
            continue
    
    print("\nCopy complete!")
    
    # Report on errors if any occurred
    if errors:
        print(f"\nWarning: {len(errors)} errors occurred during copying")
        print(f"Files copied: {files_copied}, Files skipped: {files_skipped}")
        print(f"Directories created: {dirs_created}, Directories skipped: {dirs_skipped}")
        print("\nFirst few errors:")
        for e in errors[:5]:  # Show only the first 5 errors to avoid cluttering the output
            print(f"- {e}")
        if len(errors) > 5:
            print(f"... and {len(errors) - 5} more errors")
            
        # Suggest running as admin if permission errors occurred
        if not is_admin() and any("Permission denied" in err for err in errors):
            print("\nTo copy system files and avoid permission errors, run this script as Administrator")
    
    return files_copied, dirs_created, files_skipped, dirs_skipped

def main():
    print("Directory Copying Utility")
    print("-" * 30)
    
    # Check for admin privileges
    if not is_admin() and sys.platform.startswith('win'):
        print("Note: For copying system files and avoiding permission errors, ")
        print("      consider running this script as Administrator.")
        print("-" * 30)
    
    # Select source directory
    print("Select source directory:")
    source_dir = select_directory("Select Source Directory")
    if not source_dir:
        print("No source directory selected. Exiting.")
        return
    
    # Select destination directory
    print("Select destination directory:")
    dest_dir = select_directory("Select Destination Directory")
    if not dest_dir:
        print("No destination directory selected. Exiting.")
        return
    
    print(f"\nCopying files from:")
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")
    
    try:
        # Perform the copy
        files_copied, dirs_created, files_skipped, dirs_skipped = copy_directory_contents(source_dir, dest_dir)
        print(f"\nOperation completed!")
        print(f"Files copied: {files_copied}")
        print(f"Directories created: {dirs_created}")
        if files_skipped > 0 or dirs_skipped > 0:
            print(f"Files skipped: {files_skipped}")
            print(f"Directories skipped: {dirs_skipped}")
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
