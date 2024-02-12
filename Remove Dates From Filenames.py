import os
import re

# Replace 'your/directory/path' with the path to the directory you want to search
directory_path = r'C:\BabelfishCompass\SQLCreateCrawler\ToDeploy'

# Regex pattern to match '_YYYYMMDD' before the file extension
date_pattern = re.compile(r'(_\d{8})(\.\w+)$')

# Loop through the files in the specified directory
for filename in os.listdir(directory_path):
    # Check if the file name ends with '_YYYYMMDD'
    match = date_pattern.search(filename)
    if match:
        # Extract the file extension
        file_extension = match.group(2)
        # New file name without the last 9 characters but with the original extension
        new_filename = date_pattern.sub(file_extension, filename)
        # Full path for the old and new file names
        old_file_path = os.path.join(directory_path, filename)
        new_file_path = os.path.join(directory_path, new_filename)

        # Print out what would be changed
        print(f'Would rename "{filename}" to "{new_filename}"')

        # Uncomment the next line to actually perform the renaming after confirming the changes
        # os.rename(old_file_path, new_file_path)