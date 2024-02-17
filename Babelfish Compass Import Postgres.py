"""
Babelfish Compass SQL Processor

Description:
This script automates the process of running Babelfish Compass commands on SQL files located within a specified directory. It processes each SQL file, imports the data to a PostgreSQL database, and logs the operation in the bbfcompass_history table.

Features:
- Traverses a specified directory to find SQL files.
- Executes Babelfish Compass commands for each found SQL file.
- Inserts operation data into the bbfcompass_history table in a PostgreSQL database.

Usage:
Set the `user_provided_directory` and `babelfish_compass_directory` variables to the respective directories before running the script.

Requirements:
- Python 3.6 or later
- psycopg2 library for PostgreSQL database connection
- Babelfish Compass installed and accessible via command line

Author: [Your Name]
Last Modified: [Date]

"""

import os
import subprocess
import psycopg2

# Hardcoded directory paths
user_provided_directory = r"C:\\a\bamplus-postgres-research-main\bamplus-postgres-research-main\Workstation-036-DDL"
babelfish_compass_directory = r"C:\\BabelfishCompass"

def run_babelfish_commands(sql_file, babelfish_compass_directory):
    # Extract the file name without extension
    file_name_without_extension = os.path.splitext(os.path.basename(sql_file))[0]

    # Define the command for processing the SQL file
    process_command = f'BabelfishCompass.bat {file_name_without_extension} {sql_file}'
    import_command = f'BabelfishCompass.bat {file_name_without_extension} -pgimport "localhost,5432,postgres,password!,test_db"'

    # Run the commands from the specified BabelfishCompass directory
    subprocess.run(process_command, shell=True, check=True, cwd=babelfish_compass_directory)
    subprocess.run(import_command, shell=True, check=True, cwd=babelfish_compass_directory)

def insert_into_bbfcompass_history():
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(host="localhost", database="test_db", user="postgres", password="password!")
    cur = conn.cursor()

    # SQL statement to be executed
    insert_sql = "INSERT INTO public.bbfcompass_history SELECT * FROM public.bbfcompass;"
    
    cur.execute(insert_sql)
    conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

def process_sql_files(directory, babelfish_compass_directory):
    # Loop through all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".sql"):
                sql_file_path = os.path.join(root, file)
                print(f"Processing {sql_file_path}...")
                # Run Babelfish Compass commands with the variable directory
                run_babelfish_commands(sql_file_path, babelfish_compass_directory)
                # Insert data into bbfcompass_history
                insert_into_bbfcompass_history()
                print(f"Completed processing {sql_file_path}.")

if __name__ == "__main__":
    process_sql_files(user_provided_directory, babelfish_compass_directory)
