"""
SQL Object ID Check Generator

Description:
    This script automates the process of scanning through .sql files within specified directories
    to identify CREATE statements for various SQL objects (e.g., tables, views, functions, procedures).
    It extracts the object names and types from these statements and generates a report that lists
    each object's type, name, and the source file. This tool is particularly useful for database
    administrators and developers who need to audit SQL scripts for object creation patterns or
    ensure that scripts do not inadvertently recreate existing objects in a database.

Usage:
    - Update the 'directories' list with the paths to the directories containing your .sql files.
    - Specify the 'output_dir' where the output file containing the object ID checks will be saved.
    - Ensure the 'encodings' list contains all encodings you wish to try when opening .sql files.
    - Run the script. It will process all .sql files in the specified directories and output a
      single file in the specified output directory, named with a timestamp indicating when the
      script was run.

Features:
    - Searches for .sql files in specified directories and their subdirectories.
    - Supports multiple file encodings, attempting to read each file with each encoding in the list until successful.
    - Identifies CREATE statements for a predefined set of SQL object types and extracts the relevant object names.
    - Outputs a comprehensive list of the found objects, including their type, name, and the file they were found in,
      to a timestamped file for easy reference and analysis.

Note:
    The script assumes that the CREATE 
"""

import os
import re
import datetime

def find_sql_files_in_directories(directories):
    """Find all SQL files in the given directories."""
    sql_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.sql'):
                    sql_files.append(os.path.join(root, file))
    return sql_files

def try_open_file_with_encodings(file_path, encodings):
    """Attempt to open a file with different encodings until successful."""
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.readlines(), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Failed to open file {file_path} with any of the specified encodings.")

def find_create_statements(sql_file_paths, output_dir, encodings):
    """Generate object ID checks for CREATE statements in SQL files, handling different encodings."""
    create_types = [
        "CREATE TYPE", "CREATE TABLE", "CREATE VIEW", "CREATE FUNCTION",
        "CREATE SYNONYM", "CREATE PROCEDURE", "CREATE SEQUENCE",
        "CREATE TRIGGER", "CREATE CONSTRAINT", "CREATE CLUSTERED INDEX",
        "CREATE INDEX", "CREATE NONCLUSTERED INDEX", "CREATE UNIQUE CLUSTERED",
        "CREATE UNIQUE NONCLUSTERED", "CREATE CLUSTERED INDEX"
    ]

    object_id_checks = []

    for sql_file_path in sql_file_paths:
        try:
            lines, used_encoding = try_open_file_with_encodings(sql_file_path, encodings)

            for line in lines:
                if any(create_type in line for create_type in create_types):
                    match = re.search(r'\[(.*?)\](?:\.\[(.*?)\])?', line)
                    if match:
                        full_object_name = '.'.join(filter(None, match.groups())).lower()
                        object_type = line.strip().split()[1].lower()
                        filename_no_ext = os.path.splitext(os.path.basename(sql_file_path))[0]

                        object_id_check = f"{object_type},{full_object_name},{filename_no_ext}\n"
                        object_id_checks.append(object_id_check)

        except Exception as e:
            print(f"Error processing {sql_file_path} with encoding {used_encoding}: {e}")

    # Output file
    output_file_path = os.path.join(output_dir, f"object_id_checks_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(object_id_checks)
    print(f"Output written to {output_file_path}")

encodings = ['utf-8-sig', 'utf-8', 'latin-1']
directories = [
    r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\new_install_before\\'
    # Add other directories as needed
]

output_dir =  r'C:\BabelfishCompass\Python Scripts\Output\\' 

# Find SQL files in directories
sql_file_paths = find_sql_files_in_directories(directories)

# Generate object ID checks
find_create_statements(sql_file_paths, output_dir, encodings)
