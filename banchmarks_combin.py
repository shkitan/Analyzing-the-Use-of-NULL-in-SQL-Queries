import os

def process_sql_files(base_dir, output_file):
    global_counter = 1
    with open(output_file, 'w') as outfile:
        # Iterate through directories inside base_dir
        for dir_name in os.listdir(base_dir):
            dir_path = os.path.join(base_dir, dir_name)
            if os.path.isdir(dir_path):
                # Iterate through the files in each directory
                for file_name in os.listdir(dir_path):
                    if file_name.endswith('.sql'):
                        file_path = os.path.join(dir_path, file_name)
                        with open(file_path, 'r') as infile:
                            content = infile.read()

                        new_identifier = f"--Q{global_counter} - {dir_name}\n"
                        # Find the first line starting with '--' and replace it
                        lines = content.splitlines()
                        for i, line in enumerate(lines):
                            if line.startswith('--'):
                                lines[i] = new_identifier
                                global_counter += 1

                        outfile.write('\n'.join(lines) + '\n\n')



if __name__ == "__main__":
    base_dir = "bancmarks"  # The directory containing subdirectories (ssb, tcph, etc.)
    output_file = "benchmarks.sql"
    process_sql_files(base_dir, output_file)
