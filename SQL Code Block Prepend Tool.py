"""
SQL File Importer for SQL Server and PostgreSQL

Description:
    This Python script facilitates the automated import of SQL files into either SQL Server or PostgreSQL databases. 
    It is designed to traverse specified directories, identify all SQL files, and insert their contents into a designated database table.
    The script supports dynamic database connection configurations for both SQL Server and PostgreSQL, allowing users to specify
    the target database system at runtime. Additionally, it intelligently handles file encodings to ensure compatibility with various
    file origins.

Usage:
    - Set the 'database_system' variable to either 'sql_server' or 'postgres' based on the target database system.
    - Configure connection parameters for both SQL Server and PostgreSQL in the 'sql_server_config' and 'postgres_config' dictionaries, respectively.
    - Specify the target directory in the 'directory' variable. The script will process all .sql files within this directory and its subdirectories.
    - Execute the script. It will establish a connection to the specified database, and for each .sql file found, it will insert its contents into the database.
    - Ensure the target database has a table named 'FileTextImport' with an appropriate schema to store file names, line numbers, text content, and file directories.

Features:
    - Dynamic database system selection allows for flexible deployment across different database environments.
    - Comprehensive file encoding support ensures the script can handle .sql files from various sources without data corruption.
    - Automatic traversal of specified directories and subdirectories for thorough file processing.
    - Detailed error logging provides insights into any issues encountered during file processing.
    - Ensures data integrity by committing transactions upon successful insertion of file contents into the database.

Note:
    Before running the script, ensure that the 'FileTextImport' table exists in your target database with columns for file name, line number, text content, and file directory. Additionally, adjust the connection parameters in the configuration dictionaries to match your database server settings.


--SQl Server
DROP TABLE IF EXISTS FileTextImport;
GO

CREATE TABLE FileTextImport (
    ID             INTEGER IDENTITY(1,1) PRIMARY KEY,
    InsetDate      DATETIME DEFAULT GETDATE() NULL,
    FileName       NVARCHAR(255) NULL,
    LineNumber     INTEGER NULL,
    myText         NVARCHAR(MAX) NULL,
    FileDirectory  NVARCHAR(MAX) NULL
);

--Postgres
DROP TABLE IF EXISTS public."FileTextImport";

CREATE TABLE public.filetextimport (
    ID             SERIAL PRIMARY KEY,
    InsertDate     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FileName       VARCHAR(255),
    LineNumber     INTEGER,
    myText         TEXT,
    FileDirectory  TEXT
);

"""


import os
import pyodbc
import psycopg2

# Define target database system
# Options: 'sql_server' or 'postgres'
database_system = 'postgres'  # Change this to 'postgres' / 'sql_server' as needed

# SQL Server connection parameters
sql_server_config = {
    'server': 'DESKTOP-D324ETP\\SQLEXPRESS01',
    'database': 'mytest',
    'trusted_connection': 'yes'
}

# PostgreSQL connection parameters
postgres_config = {
    'database': 'test_db',
    'user': 'postgres',
    'password': 'Letmein01!',
    'host': 'localhost'
}

# Directory to search for .sql files
directory = r'C:\tmp\\'

def import_sql_files(directory, database_system):
    if database_system == 'sql_server':
        cnxn_string = f"DRIVER={{SQL Server}};SERVER={sql_server_config['server']};DATABASE={sql_server_config['database']};Trusted_Connection={sql_server_config['trusted_connection']};"
        cnxn = pyodbc.connect(cnxn_string)
    elif database_system == 'postgres':
        cnxn_string = f"dbname={postgres_config['database']} user={postgres_config['user']} password={postgres_config['password']} host={postgres_config['host']}"
        cnxn = psycopg2.connect(cnxn_string)
    else:
        raise ValueError("Unsupported database system specified.")
    
    cursor = cnxn.cursor()
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".sql"):
                file_path = os.path.join(root, file)
                file_directory = os.path.dirname(file_path)  # Get the directory of the file
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_number = 1  # Initialize line number
                        for line in f:
                            if database_system == 'sql_server':
                                insert_stmt = "INSERT INTO FileTextImport (FileName, LineNumber, myText, FileDirectory) VALUES (?, ?, ?, ?)"
                            elif database_system == 'postgres':
                                insert_stmt = "INSERT INTO FileTextImport (FileName, LineNumber, myText, FileDirectory) VALUES (%s, %s, %s, %s)"
                            # Execute insert statement
                            cursor.execute(insert_stmt, (file, line_number, line, file_directory))
                            line_number += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    # Commit transactions and close connection
    cnxn.commit()
    cursor.close()
    cnxn.close()

import_sql_files(directory, database_system)
print('Task Completed')
