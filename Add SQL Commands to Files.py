"""
SQL Code Block Prepend Tool

Description:
    This script automates the process of prepending a specific SQL code block to all .sql files within
    specified directories. It supports multiple predefined code block options, allowing the user to
    select which block to prepend based on their requirements. The script also handles file encoding
    intelligently, ensuring that the prepend action respects the original file's encoding. This feature
    is particularly useful for preparing SQL files with necessary configurations or statements before
    execution in different environments.

Usage:
    - Define the SQL code block options within the 'options' dictionary. Each option should be a complete,
      ready-to-prepend SQL statement or set of statements.
    - Set the 'option_to_use' variable to the key of the desired code block from the 'options' dictionary.
    - Specify the directories to be processed in the 'directories' list. All .sql files within these directories
      (and their subdirectories) will be processed.
    - Run the script. It will prepend the chosen SQL code block to each .sql file, handling various encodings
      and ensuring that the file's original encoding is preserved.

Features:
    - Allows specification of multiple SQL code block options for different use cases.
    - Prepends chosen SQL code block to the beginning of each .sql file in the specified directories.
    - Handles file encodings ('utf-8-sig', 'utf-8', 'latin-1') to accommodate files from different sources.
    - Checks if a file already starts with one of the options and, if so, replaces it with the chosen option to avoid duplication.
    - Provides feedback on the processing of each file, including the file path and encoding used.

Note:
    Before running this script, ensure that you have backups of your .sql files, as this process modifies the files in place.
    Modify the 'options' dictionary and the 'directories' list according to your specific 

import os
import re
"""

# Define your options here
options = {
    'option1': """
USE bsav2_MyTest_DB;  --Babelfish addition: Setting this for testing.
GO
SET NOCOUNT ON;
GO
""",
    'option2': """
USE bsav2_MyTest_DB;  --Babelfish addition: Setting this for testing.
GO
EXECUTE sp_babelfish_configure '%', 'ignore', 'server'--Babelfish addition: Setting this for testing.
GO
SET NOCOUNT ON;
GO
""",
    'option3': """
EXECUTE sp_babelfish_configure '%', 'ignore', 'server'--Babelfish addition: Setting this for testing.
GO
"""
}
import os
import re

def prepend_code_block_with_encoding_handling(directories, chosen_option, encodings, options):
    """
    Prepends a given code block to all .sql files in the specified directories,
    taking into account the file's encoding to handle UTF properly.
    """
    combined_options_pattern = re.compile('|'.join(re.escape(opt) for opt in options.values()), re.DOTALL)

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".sql"):
                    file_path = os.path.join(root, file)
                    file_content, encoding_used = read_file_with_encoding_detection(file_path, encodings)

                    # Check if the file content starts with any of the options
                    if combined_options_pattern.match(file_content):
                        new_content = combined_options_pattern.sub('', file_content).lstrip()
                        new_content = chosen_option.rstrip() + "\n\n" + new_content
                    else:
                        new_content = chosen_option.rstrip() + "\n\n" + file_content

                    with open(file_path, 'w', encoding=encoding_used) as f:
                        f.write(new_content)
                    print(f"Processed {file_path} with encoding {encoding_used}")

def read_file_with_encoding_detection(file_path, encodings):
    """
    Attempts to read a file with multiple encodings until one succeeds.
    Returns the file content and the encoding used.
    """
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read(), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Failed to decode {file_path} with given encodings.")

if __name__ == "__main__":
    encodings = ['utf-8-sig', 'utf-8', 'latin-1']
    
    #Set you option!!!
    #Set you option!!!
    #Set you option!!!
    option_to_use = 'option1'  # for example
    code_block = options[option_to_use]

    directories = [
        r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\new_install_before\\'
        #,r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\bsav2_upgrade\\'
        #,r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\before_every_upgrade\\'
        #,r'C:\b\bamplus-postgres-research-main\bamplus-postgres-research-main\Bam+ Installer\module-packages\BAMPlus.BAM.Bridge\database\after_every_upgrade\\'
    ]

    prepend_code_block_with_encoding_handling(directories, code_block, encodings, options)
    print("Done processing .sql files.")
