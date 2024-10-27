import math
import re
import json
from collections import defaultdict
from analysis_misuse_null import *
min_complexity = math.inf
max_complexity = -1
import pandas as pd

# Load the queries from a JSON file
def load_queries_from_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        queries = json.load(file)
    return queries

# Analyze the complexity of each query
def categorize_by_complexity(query):
    complexity = 0

    # Count JOINs
    joins = len(re.findall(r'\bJOIN\b', query, re.IGNORECASE))
    if joins > 0:
        complexity += joins * 0.5  # More joins add more complexity

    # Subqueries
    subqueries = len(re.findall(r'\bSELECT\b.*\bFROM\b', query, re.IGNORECASE)) - 1
    if subqueries > 0:
        complexity += 2 * subqueries  # Subqueries increase complexity significantly

    # Grouping and Ordering
    if re.search(r'\bGROUP BY\b', query, re.IGNORECASE):
        complexity += 1
    if re.search(r'\bORDER BY\b', query, re.IGNORECASE):
        complexity += 1

    # HAVING clauses
    if re.search(r'\bHAVING\b', query, re.IGNORECASE):
        complexity += 1

    global min_complexity
    global max_complexity
    min_complexity = min(min_complexity, complexity)
    max_complexity = max(max_complexity, complexity)
    return complexity

# Detect NULL handling in queries
def detect_null_handling(query):
    null_handling = {
        'IS NULL': len(re.findall(r'\bIS NULL\b', query, re.IGNORECASE)),
        'IS NOT NULL': len(re.findall(r'\bIS\s*NOT\s*NULL\b', query, re.IGNORECASE)),
        'NULL in JOIN': len(re.findall(r'JOIN\b.*?\bIS NULL\b', query,
                                       re.IGNORECASE)) + len(re.findall(
            r'JOIN\b.*?\bIS NOT NULL\b', query, re.IGNORECASE)),
        'IFNULL': len(re.findall(r'\bIFNULL\b', query, re.IGNORECASE)),
        'COALESCE': len(re.findall(r'\bCOALESCE\b', query, re.IGNORECASE))
    }
    return null_handling

def count_null_bag_cases(query):
    null_bag_cases = {
        'null_comparing_case1': misuse_counting_case1(query),
        'sum_coalesce_pattern_case2': misuse_counting_case2(query),
        'where_not_in_pattern_case3': misuse_counting_case3(query),
        'count_null_case4': misuse_counting_case4(query),
        'math_operation_case5': misuse_counting_case5(query)
    }
    return null_bag_cases

from itertools import islice

def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

def add_row(dataframe, row_data):
    # Create a DataFrame from the row data
    new_row = pd.DataFrame([row_data], columns=dataframe.columns)
    # Append the new row to the existing DataFrame
    return pd.concat([dataframe, new_row], ignore_index=True)

# Perform analysis on all queries
def analyze_queries(queries, csv_name):
    columns = ['query_id', 'complexity', 'IS NULL counting', 'IS NOT NULL counting',
               'NULL in JOIN counting', 'IFNULL counting', 'COALESCE counting',
               'null_comparing_case1 counting',
               'sum_coalesce_pattern_case2 counting', 'where_not_in_pattern_case3 counting',
               'count_null_case4 counting', 'math_operation_case5 counting']
    df = pd.DataFrame(columns=columns)

    for query_num, query in queries.items():

        # Categorize by complexity
        complexity = categorize_by_complexity(query)

        # Analyze NULL handling
        # null_handling = detect_null_handling(query)
        #
        # null_bags = count_null_bag_cases(query)
        df = add_row(df, {
            'query_id': query_num,
            'complexity': complexity,
            'IS NULL counting': len(re.findall(r'\bIS\s*NULL\b', query,
                                       re.IGNORECASE)),
            'IS NOT NULL counting': len(re.findall(r'\bIS\s*NOT\s*NULL\b', query,
                                           re.IGNORECASE)),
            'NULL in JOIN counting': len(re.findall(r'\b(INNER|LEFT|RIGHT)(\s+OUTER)?\s+JOIN\b', query,
                                           re.IGNORECASE)),
            'IFNULL counting': len(re.findall(r'\bIFNULL\b', query, re.IGNORECASE)),
            'COALESCE counting': len(re.findall(r'\bCOALESCE\b', query,
                                                re.IGNORECASE)),
            'null_comparing_case1 counting': misuse_counting_case1(query),
            'sum_coalesce_pattern_case2 counting': misuse_counting_case2(query),
            'where_not_in_pattern_case3 counting': misuse_counting_case3(query),
            'count_null_case4 counting': misuse_counting_case4(query),
            'math_operation_case5 counting': misuse_counting_case5(query)
        })

    df.to_csv(f'{csv_name}.csv', index=False)

def save_analyis_results_to_file(results, output_file):
    import json
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)

def print_min_max_complex():
    global min_complexity
    global max_complexity
    print("the max complexity is %d", max_complexity)
    print("the min complexity is %d", min_complexity)

# Main function to load, analyze, and print results
def main():
    input_file_benchmark_queries = 'benchmark_queries.json'
    benchmark_queries = load_queries_from_file(input_file_benchmark_queries)
    analysis_results_benchmark_queries = analyze_queries(benchmark_queries,
                                                         "benchmark_queries")
    save_analyis_results_to_file(analysis_results_benchmark_queries, "analysis_results_benchmark_queries.json")

    # input_file_queries_github_dataset = 'queries.json'
    # queries_github_dataset = load_queries_from_file(input_file_queries_github_dataset)
    # analysis_results_queries_github_dataset = analyze_queries(
    #     queries_github_dataset,
    #     "queries_github_dataset")
    # save_analyis_results_to_file(analysis_results_queries_github_dataset, "analysis_results_queries_github_dataset.json")



# Run the main function
if __name__ == "__main__":
    main()
