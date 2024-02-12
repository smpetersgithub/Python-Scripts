"""
SQLCMD Script Generator

Description:
    This script generates an SQLCMD script to execute .sql files found within specified directories.
    It automatically traverses through each directory, compiles commands to execute found .sql files,
    and copies the final SQLCMD script to the clipboard.

Usage:
    Modify the 'directories' list in the '__main__' section to include the paths to the directories
    containing your .sql files. 
    
Features:
    - Traverses specified directories for .sql files.
    - Generates SQLCMD script commands for executing the found .sql files.
    - Supports outputting the script to the clipboard.

Note:
    This script requires the 'pyperclip' module for clipboard functionality. Ensure it is installed
    via 'pip install pyperclip' before running the script.
"""

import os
import pyperclip

def generate_sqlcmd_script(directories):
    """
    Generates an SQLCMD script to execute .sql files in specified directories and
    copies the script to the clipboard.

    Parameters:
    directories (list): A list of directory paths containing .sql files to execute.
    """
    sqlcmd_script_content = "SET NOCOUNT ON;\nGO\nPRINT @@SERVERNAME;\nGO\n\n"
    
    for directory in directories:
        path_var = f":setvar Path \"{directory}\"\n\n"
        sqlcmd_script_content += path_var

        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.sql'):
                    # Extract the last folder name from the directory path
                    last_folder_name = os.path.basename(os.path.normpath(directory))
                    sqlcmd_script_content += f"PRINT('Executing {last_folder_name}/{filename}')\n"
                    sqlcmd_script_content += f":setvar SQLFile \"{filename}\"\n"
                    sqlcmd_script_content += ":r $(Path)$(SQLFile)\nGO\n\n"

    # Copy the generated SQLCMD script to the clipboard
    pyperclip.copy(sqlcmd_script_content)
    print("SQLCMD script has been copied to the clipboard.")

if __name__ == "__main__":
    # List of directories containing .sql files
    directories = [
        r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\new_install_before\\'
        #r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\before_every_upgrade\\'
        #r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\bsav2_upgrade\\'
        #r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\after_every_upgrade\\'
    ]
    generate_sqlcmd_script(directories)
