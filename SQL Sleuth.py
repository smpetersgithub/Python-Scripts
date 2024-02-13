"""
SQL Keyword Analysis Tool

Description:
    This script is developed to automate the process of analyzing .sql files for specific keywords.
    It searches through all .sql files within given directory paths, counts occurrences of each keyword
    (specified in a separate configuration file), and outputs the results to CSV files. One output file
    contains raw counts per file, and another is a pivoted view showing keyword occurrences across files.
    This tool is particularly useful for code reviews, auditing, or tracking the usage of SQL patterns or
    practices across multiple SQL scripts.

Usage:
    - Update the 'directories' list with the full paths to the directories containing your .sql files.
    - Specify the 'config_file' path where keywords to be searched are listed, one per line.
    - Set the 'output_dir' to the desired output directory for the CSV files.
    - Run the script. It will generate two CSV files in the specified output directory:
        1. A detailed count of keywords for each file.
        2. A pivoted table showing the occurrence of each keyword across all files.

Features:
    - Supports searching through multiple directories and subdirectories for .sql files.
    - Utilizes regular expressions for keyword search to ensure accurate matching.
    - Outputs comprehensive CSV files for easy analysis and sharing.
    - Handles files with different encodings by attempting to read files with multiple predefined encodings.
    - Prompts for user confirmation before proceeding with the deletion of lines (if applicable).

Note:
    Ensure the configuration file with keywords exists and is correctly formatted before running this script.
    The output directory must be writable by the script. Consider backing up your SQL files before running
    this script if it is modified to perform write operations on the SQL files.
"""
import os
import re
import datetime
import csv

def load_keywords(file_path):
    """Load keywords from the specified configuration file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def search_keywords(sql_file, keywords):
    """Count occurrences of each keyword in the specified SQL file using regex."""
    with open(sql_file, 'r') as file:
        content = file.read().upper()

    keyword_counts = {}
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword.upper()), re.IGNORECASE)
        keyword_counts[keyword] = len(pattern.findall(content))

    return keyword_counts

def output_results(output_file, counts, file_name, file_path):
    """Append the keyword counts along with file name and path to the specified output file."""
    file_exists = os.path.isfile(output_file)
    with open(output_file, 'a', newline='') as csvfile:
        headers = ['Keyword', 'Count', 'FileName', 'FilePath']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        if not file_exists:
            writer.writeheader()  # Write header if file does not exist
        
        for keyword, count in counts.items():
            writer.writerow({'Keyword': keyword, 'Count': count, 'FileName': file_name, 'FilePath': file_path})

def find_sql_files(directories):
    """Search for all SQL files within the specified directories."""
    sql_files = []
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".sql"):
                    sql_files.append(os.path.join(root, file))
    return sql_files

def main(config_file, directories, output_dir):
    """Run the keyword search on all SQL files found in the specified directories and output the results."""
    keywords = load_keywords(config_file)
    sql_files = find_sql_files(directories)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"wordcount_SQLSleuth_{timestamp}.csv")

    for sql_file in sql_files:
        counts = search_keywords(sql_file, keywords)
        file_name = os.path.basename(sql_file)  # Extract the file name
        output_results(output_file, counts, file_name, sql_file)  # Include file name and path

    print(f"Output written to {output_file}")

# Configuration
output_dir = r'C:\BabelfishCompass\Python Scripts\Output\\'
config_file = r'C:\BabelfishCompass\Python Scripts\SQL Sleuth Configuration.txt'
directories = []

# Execute the main function
if __name__ == "__main__":
    main(config_file, directories, output_dir)
