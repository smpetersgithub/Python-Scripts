"""
SQL File Pattern Replacement Tool

Description:
    This script facilitates the batch updating of SQL files across multiple directories,
    replacing specified search patterns with a new string. It's particularly useful for
    renaming database identifiers, schema names, or updating SQL commands en masse within
    a large set of SQL scripts. The script iterates over each file in the specified directories,
    searches for the given pattern using regular expressions, and replaces all occurrences
    with the provided replacement string.

Usage:
    - Define the 'search_pattern' with a regular expression that matches the text you wish to replace.
    - Set the 'replacement_string' to the text that will replace each occurrence of the search pattern.
    - List all target directories in the 'directories' list where the SQL files are located.
    - Specify the 'encodings' list with the encodings to try when opening and saving files, accommodating
      different file encoding standards for compatibility.
    - Run the script. It will recursively search through each directory, replacing the pattern in all files found.

Features:
    - Supports multiple encodings for reading and writing files, ensuring wide compatibility with different file formats.
    - Uses regular expressions for pattern matching, providing flexibility in defining the search pattern.
    - Performs in-place file updates, directly modifying the original files with the new content.
    - Prints a message for each file that is updated, providing a clear log of changes made.

Note:
    It is highly recommended to backup your files before running this script, as it modifies the files in place.
    Ensure that the search pattern correctly matches only the intended occurrences to prevent unintended replacements.
    The script does not modify filenames or directory names, only the contents of the files.

"""
import os
import re

def replace_in_file(file_path, search_pattern, replacement, encodings):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                file_contents = f.read()

            # Replace occurrences
            new_contents = re.sub(search_pattern, replacement, file_contents)

            # If changes were made, write the file
            if new_contents != file_contents:
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(new_contents)
                print(f"Updated {file_path}")
            # Stop after successfully reading and writing the file
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            break

def replace_in_files(directories, search_pattern, replacement, encodings):
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                replace_in_file(file_path, search_pattern, replacement, encodings)

if __name__ == "__main__":
    
    # Find this string
    search_pattern = r'bsav2_{BankId}'
    
    # and replace it with this string
    replacement_string = 'bsav2_mytest_db'
    
    encodings = ['utf-8-sig', 'utf-8', 'latin-1']

    directories = [
        r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\new_install_before\\'
        ,r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\bsav2_upgrade\\'
        ,r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\before_every_upgrade\\'
        ,r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\after_every_upgrade\\'
        ]
    
    replace_in_files(directories, search_pattern, replacement_string, encodings)
    print("Done processing all directories.")
