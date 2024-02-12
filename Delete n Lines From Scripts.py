import os

def confirm_action(num_lines, directories):
    """
    Prompts the user for confirmation to proceed with the action.
    """
    print(f"You are about to delete the first {num_lines} lines from all .sql files in the following directories:")
    for directory in directories:
        print(directory)
    return input("Do you want to proceed? (yes/no): ").strip().lower() == "yes"

"""
SQL File Line Deletion Tool

Description:
    This script is designed to remove the first N lines from all `.sql` files within specified directories.
    It aims to automate the preparation of SQL files by deleting unnecessary header information or comments
    that may be present at the beginning of these files. The script supports multiple file encodings, attempting
    to read and write files with different encoding standards to ensure compatibility across various file formats.

Usage:
    - Update the 'directories' list in the '__main__' section with the paths to the directories containing your .sql files.
    - Set the 'num_lines_to_delete' variable to specify the number of lines you wish to remove from the beginning of each file.
    - Run the script. You will be prompted to confirm the deletion action before it proceeds.

Features:
    - Iterates over specified directories to find .sql files.
    - Prompts user for confirmation before performing deletions.
    - Attempts to handle files with multiple encodings, specifically 'utf-8' and 'latin-1', to accommodate various file origins.
    - Provides feedback on processing status and encoding issues encountered.

Note:
    It is recommended to backup your .sql files before running this script to prevent accidental data loss.
    Ensure you have write permissions for the directories and files you intend to process.
"""

def delete_first_n_lines(directories, num_lines, encodings=('utf-8', 'latin-1')):
    """
    Deletes the first n lines from all .sql files in the specified directories,
    trying multiple encodings in case of UnicodeDecodeErrors.
    """
    if not confirm_action(num_lines, directories):
        print("Operation canceled.")
        return
    
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".sql"):
                    file_path = os.path.join(root, file)
                    for encoding in encodings:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                lines = f.readlines()
                            # Skip the first n lines
                            new_content = lines[num_lines:]
                            # Write the remaining content back to the file
                            with open(file_path, 'w', encoding=encoding) as f:
                                f.writelines(new_content)
                            print(f"Processed {file_path} with encoding {encoding}")
                            break  # Stop trying encodings if successful
                        except UnicodeDecodeError as e:
                            print(f"Error decoding {file_path} with {encoding}: {e}")
                            if encoding == encodings[-1]:  # Last encoding option
                                print(f"Failed to process {file_path} due to encoding issues.")

if __name__ == "__main__":
    # Directories to process
    directories = [
        #r'C:\a\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\new_install_before\\'
        #,r'C:\a\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\before_every_upgrade\\'
        #,r'C:\a\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\bsav2_upgrade\\'
        #, r'C:\a\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\after_every_upgrade\'    ]    
    ]
    num_lines_to_delete = 6  # Adjust the number of lines you want to delete

    delete_first_n_lines(directories, num_lines_to_delete)
    print("Done processing .sql files.")
