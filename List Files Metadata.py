import os

def find_sql_files(directory, output_file):
    """
    This function walks through a directory and its subdirectories,
    writing the results of the analysis, including the file encoding, to an output file with headers.
    """
    headers = ["File Name", "Size (bytes)", "Directory", "Encoding", "Lines", "CREATEs", "ALTERs", "INSERTs", "UPDATEs"]
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write the header row
        f.write(", ".join(headers) + "\n")
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".sql"):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    analysis, encoding_used = analyze_sql_file(file_path)
                    # Write the data row including the encoding
                    f.write(f"{file}, {file_size}, {root}, {encoding_used}, {analysis['line_count']}, {analysis['create_count']}, {analysis['alter_count']}, {analysis['insert_count']}, {analysis['update_count']}\n")

def analyze_sql_file(file_path):
    """
    Analyzes the given SQL file for the number of lines, 'CREATE' keywords,
    'ALTER', 'INSERT', and 'UPDATE' statements, and returns the encoding used.
    Attempts to open files with a robust approach to handle various encodings.
    """
    counts = {'line_count': 0, 'create_count': 0, 'alter_count': 0, 'insert_count': 0, 'update_count': 0}
    encodings = ['utf-8-sig', 'latin-1']
    file_content = None
    encoding_used = ""

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                file_content = file.readlines()
                encoding_used = encoding  # Capture the encoding successfully used
                break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Failed to read {file_path} due to an unexpected error: {e}")
            return counts, encoding_used

    if file_content:
        for line in file_content:
            counts['line_count'] += 1
            upper_line = line.upper()
            counts['create_count'] += upper_line.count('CREATE')
            counts['alter_count'] += upper_line.count('ALTER')
            counts['insert_count'] += upper_line.count('INSERT')
            counts['update_count'] += upper_line.count('UPDATE')

    return counts, encoding_used

# Set the directory and output file path
directory = r'c:\b\\'
output_file = r"C:\BabelfishCompass\Python Scripts\Output\FileAnalysisSQL.txt"
find_sql_files(directory, output_file)

print(f"Analysis completed. Results are written to {output_file}.")
