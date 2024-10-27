import re

def extract_queries(file_path):
    queries = {}
    current_query_num = None
    current_query = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            query_num_match = re.match(r'-- Query #?(\d+)',
                                       line.strip())
            if query_num_match:
                if current_query_num is not None and current_query:
                    queries[current_query_num] = ''.join(current_query).strip()
                current_query_num = int(query_num_match.group(1))
                current_query = []
            else:
                current_query.append(line)
        if current_query_num is not None and current_query:
            queries[current_query_num] = ''.join(current_query).strip()

    return queries


def save_queries_to_file(queries, output_file):
    import json
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(queries, file, indent=4)


def load_queries_from_file(input_file):
    import json
    with open(input_file, 'r', encoding='utf-8') as file:
        queries = json.load(file)
    return queries


# sql_file = 'combined_cleaned_recounted_queries.sql'
# output_file = 'queries.json'
# queries = extract_queries(sql_file)
# save_queries_to_file(queries, output_file)

sql_file = 'benchmark_queries.sql'
output_file = 'benchmark_queries.json'

# Extract queries from SQL file and save to JSON
queries = extract_queries(sql_file)
save_queries_to_file(queries, output_file)
