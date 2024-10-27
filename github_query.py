import requests
import os
import re

GITHUB_API_SEARCH_URL = "https://api.github.com/search/code"

# Your GitHub personal access token (replace with your actual token)
GITHUB_TOKEN = "todo: add your own token"

core_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "JOIN", "WHERE", "GROUP BY", "ORDER BY"]
procedural_keywords = ["GO", "FOR", "COMMIT", "ROLLBACK", "BEGIN", "END", "DECLARE", "EXEC", "EXECUTE"]

def is_core_sql(content):
    """Check if content contains only core SQL queries."""
    content_upper = content.upper()
    if any(keyword in content_upper for keyword in procedural_keywords):
        return False
    return any(keyword in content_upper for keyword in core_keywords)

def extract_queries(content):
    """Extract individual queries from content."""
    queries = re.split(r';\s*', content)
    return [query.strip() for query in queries if query.strip()]

def fetch_sql_files_from_github(query, page, per_page):
    """Fetch SQL files from GitHub via API with specific keyword query."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'SQL-Query-Script',
        'Authorization': f'token {GITHUB_TOKEN}'  # Add token for authentication
    }
    params = {
        'q': f'{query} extension:sql',
        'page': page,
        'per_page': per_page
    }
    response = requests.get(GITHUB_API_SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def download_raw_file(file_url):
    """Download the raw content of a GitHub file."""
    response = requests.get(file_url)
    response.raise_for_status()
    return response.text

def combine_core_queries_from_github(output_file, max_queries,
                                     max_pages, per_page):
    """Combine core SQL queries from GitHub files into one big file with a global counter."""
    global_counter = 0

    sql_queries_to_search = [
        "SELECT", "INSERT", "UPDATE", "DELETE", "JOIN", "INNER JOIN", "LEFT JOIN",
        "RIGHT JOIN", "FULL JOIN", "WHERE", "GROUP BY", "ORDER BY", "LIMIT", "OFFSET",
        "UNION", "UNION ALL", "HAVING", "DISTINCT", "LIKE", "BETWEEN", "IN", "IS NULL",
        "IS NOT NULL", "EXISTS", "CASE", "WHEN", "THEN", "ELSE", "COALESCE", "CAST",
        "CONVERT", "COUNT", "SUM", "AVG", "MIN", "MAX", "ROUND", "FLOOR", "CEIL",
        "ABS", "MOD", "LENGTH", "SUBSTRING", "CONCAT", "TRIM", "REPLACE", "CHAR_LENGTH",
        "POSITION", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "NOW", "DATE",
        "TIME", "YEAR", "MONTH", "DAY", "WEEK", "HOUR", "MINUTE", "SECOND", "EXTRACT",
        "DATE_ADD", "DATE_SUB", "DATEDIFF", "STR_TO_DATE", "FORMAT", "IF", "IFNULL",
        "NULLIF", "GREATEST", "LEAST", "SUBSTR", "CHAR", "ASCII", "SOUNDEX", "RAND",
        "UPPER", "LOWER", "REVERSE", "HEX", "UNHEX", "POWER", "EXP", "LOG", "SQRT",
        "SIGN", "PI", "RADIANS", "DEGREES", "TRUNCATE", "BIT_AND", "BIT_OR", "BIT_XOR",
        "ISNULL", "ROW_NUMBER", "RANK", "DENSE_RANK", "NTILE", "LEAD", "LAG", "PARTITION BY"
    ]

    with open(output_file, 'w', encoding='utf-8') as output_f:
        for sql_keyword in sql_queries_to_search:
            print(f"Searching GitHub for {sql_keyword} queries in .sql files...")
            for page in range(1, max_pages + 1):
                print(f"Fetching page {page} of SQL files for query '{sql_keyword}'...")
                search_results = fetch_sql_files_from_github(sql_keyword, page, per_page)

                for item in search_results.get('items', []):
                    raw_url = item.get('html_url').replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                    try:
                        print(f"Downloading file: {raw_url}")
                        file_content = download_raw_file(raw_url)
                    except Exception as e:
                        print(f"Failed to download {raw_url}: {e}")
                        continue

                    if is_core_sql(file_content):
                        queries = extract_queries(file_content)

                        for query in queries:
                            if global_counter > max_queries:
                                print(f"Reached maximum limit of {max_queries} queries.")
                                return
                            output_f.write(f"-- Query {global_counter}\n")
                            output_f.write(f"{query};\n\n")
                            global_counter += 1

    print(f"Successfully combined {global_counter - 1} queries into {output_file}")

output_file = "combined_core_queries.sql"
combine_core_queries_from_github(output_file, max_queries=50000000,
                                 max_pages=10,
                                 per_page=30000)
