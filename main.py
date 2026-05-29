# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return the first and last names and the job titles for all employees in Boston.

df_boston = pd.read_sql("""
    SELECT firstName, lastName, jobTitle 
    FROM employees 
    JOIN offices USING(officeCode) 
    WHERE city = 'Boston';
""", conn)

# STEP 2: Are there any offices that have zero employees?
df_zero_emp = pd.read_sql("""
    SELECT o.* FROM offices o 
    LEFT JOIN employees e ON o.officeCode = e.officeCode 
    WHERE e.employeeNumber IS NULL;
""", conn)

# STEP 3
# Replace None with your code
df_employee = None

# STEP 4
# Replace None with your code
df_contacts = None

# STEP 5
# Replace None with your code
df_payment = None

# STEP 6
# Replace None with your code
df_credit = None

# STEP 7
# Replace None with your code
df_product_sold = None

# STEP 8
# Replace None with your code
df_total_customers = None

# STEP 9
# Replace None with your code
df_customers = None

# STEP 10
# Replace None with your code
df_under_20 = None

conn.close()