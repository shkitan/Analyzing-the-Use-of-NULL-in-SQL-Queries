import re

null_comparing_case1 = r'(?:\w+\s*(?:=|!=)\s*NULL|NULL\s*(?:=|!=)\s*\w+)'
sum_coalesce_pattern_case2 = r'.*(?:SUM|COUNT|AVG)\s*\(\s*COALESCE\s*\(.*?'
where_not_in_pattern_case3 = r'.*\bWHERE\b.*\bNOT\s+IN\s*\(\s*SELECT\b.*'
count_null_case4 = r'COUNT\(\s*(?!\*|\d+\b|\w*id\w*)\s*\w+\s*\)'
math_operation_case5 = r'(SELECT|select)(\w+)\s*[\+\-\*\/]\s*(' \
                       r'?!\s*COALESCE\s*\()(\w+)(FROM|from)'

def misuse_counting(input_string, pattern):
    sum_coalesce_matches = re.findall(pattern, input_string, re.IGNORECASE)
    sum_coalesce_count = len(sum_coalesce_matches)
    return sum_coalesce_count

def misuse_counting_case1(input_string):
    return misuse_counting(input_string, null_comparing_case1)

def misuse_counting_case2(input_string):
    return misuse_counting(input_string, sum_coalesce_pattern_case2)

def misuse_counting_case3(input_string):
    return misuse_counting(input_string, where_not_in_pattern_case3)

def misuse_counting_case4(input_string):
    return misuse_counting(input_string, count_null_case4)

def misuse_counting_case5(input_string):
    return misuse_counting(input_string, math_operation_case5)


##################### test Examples ###################################

test_string1 = """
SELECT * FROM table WHERE column1 = NULL AND column2!=NULL
AND NULL = column3 AND NULL!=column4 AND column5 = NULL
"""
test_string3 = """
SELECT * FROM table WHERE column1 = NULL AND column2!=NULL
"""

test_string2 = """
SELECT 
    SUM(column1) as total1,
    (SELECT SUM(COALESCE(column2, 0)) FROM subquery) as total2,
    CASE WHEN condition THEN SUM(UpperColumn) ELSE 0 END as total3,
    SUM(COALESCE(lower_column , 0)) + 100 as total4,
    (SUM(MixedCase) + 100) * 2 as total5,
    AVG(SUM(COALESCE(camelCase, snake_case, 0))) OVER (PARTITION BY group_col) as total6
FROM table
GROUP BY group_col
"""
test_string4 = """
SELECT 
    SUM(column1) as total1,
    (SELECT AVG(COALESCE(column2, 0)) FROM subquery) as total2,
    CASE WHEN condition THEN SUM(UpperColumn) ELSE 0 END as total3,
    SUM(COALESCE(lower_column , 0)) + 100 as total4,
    (COUNT(MixedCase) + 100) * 2 as total5,
    AVG(COUNT(COALESCE(camelCase, snake_case, 0))) OVER (PARTITION BY group_col) as total6
FROM table
GROUP BY group_col
"""

test_case3_1 = """
SELECT *
FROM employees
WHERE department_id NOT IN (
    SELECT department_id
FROM departments
WHERE name IS NULL
);
"""
test_case3_2 = """
SELECT *
FROM orders
WHERE NOT EXISTS (
    SELECT 1
FROM customers
WHERE orders.customer_id = customers.customer_id
AND customers.country IS NULL
);
"""
test_case3_3 = """
SELECT *
FROM employees
WHERE department_id NOT IN (
    SELECT department_id
FROM departments
WHERE name IS NULL
)
JOIN
SELECT *
FROM people
WHERE id NOT IN (
    SELECT invalid_id
FROM ids
WHERE name IS NULL
)
;
"""

test_case4_1 = """
SELECT COUNT(salary), COUNT(*), COUNT(department_id) 
FROM employees;
"""
test_case4_2 = """
SELECT COUNT(*), COUNT(*), COUNT(*) 
FROM employees;
"""
test_case4_3 = """
SELECT COUNT(a), COUNT(b), COUNT(c) 
FROM employees;
"""

test_case5_1_1 = """
SELECT salary + bonus FROM employees;
"""
test_case5_2_3 = """
SELECT total_sales - discount FROM orders;
SELECT price * quantity FROM inventory WHERE total_cost = price * quantity;

"""
test_case5_3_0 = """
SELECT salary + COALESCE(bonus, 0) FROM employees;

"""
test_case5_4_0 = """
SELECT total_sales + COALESCE(discount, 0) FROM orders;

"""
test_case5_5_0 = """
SELECT salary + COALESCE(bonus, 0) FROM employees;

"""
test_case5_6_0 = """
SELECT salary + COALESCE(bonus, 0) FROM employees;
SELECT total_sales + COALESCE(discount, 0) FROM orders;

"""
test_case5_2_2 = """
SELECT price * quantity FROM inventory WHERE total_cost = price * quantity;

"""

##################### test Examples ###################################
