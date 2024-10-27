import os

directory_path = "bancmarks/tpch"

def add_query_identifier_to_sql_files(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".sql"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
            content.insert(0, "--Q\n")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(content)

            print(f"Added '--Q' to the first line of {filename}")

add_query_identifier_to_sql_files(directory_path)
