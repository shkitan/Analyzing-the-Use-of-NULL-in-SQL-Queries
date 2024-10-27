import os

root_directory = "bancmarks"

class SqlFileFormatError(Exception):
    """Custom exception raised when a SQL file doesn't meet the required format."""
    def __init__(self, message, file_path):
        super().__init__(message)
        self.file_path = file_path

def verify_sql_file(file_path):
    """Verify that the SQL file contains exactly one '--' and one ';'."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Count occurrences of '--' and ';'
    comment_count = content.count('--')
    semicolon_count = content.count(';')

    if comment_count != 1:
        raise SqlFileFormatError(f"File {file_path} does not contain exactly one '--' (found {comment_count}).", file_path)

    if semicolon_count != 1:
        raise SqlFileFormatError(f"File {file_path} does not contain exactly one ';' (found {semicolon_count}).", file_path)

def verify_sql_files_in_directory(directory):
    """Recursively verify SQL files in the given directory and subdirectories."""
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".sql"):
                file_path = os.path.join(dirpath, filename)
                try:
                    verify_sql_file(file_path)

                except SqlFileFormatError as e:
                    print(f"Error: {e}")


verify_sql_files_in_directory(root_directory)
