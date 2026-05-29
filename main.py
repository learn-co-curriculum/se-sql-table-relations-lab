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

# STEP 3: Return employees' first/last name and city/state of their office. Include all employees, order by first then last name.
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state 
    FROM employees e 
    LEFT JOIN offices o ON e.officeCode = o.officeCode 
    ORDER BY e.firstName, e.lastName;
""", conn)

# STEP 4: Customer contact info and sales rep employee number for customers who haven't placed an order. Sorted by contact's last name.
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber 
    FROM customers c 
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber 
    WHERE o.orderNumber IS NULL 
    ORDER BY c.contactLastName;
""", conn)

# STEP 5: Customer contacts, payment amounts, and dates of payment. Sorted DESC by amount. (Hint used: CAST amount to numeric).
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate 
    FROM customers c 
    JOIN payments p ON c.customerNumber = p.customerNumber 
    ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)

# STEP 6: Employee details and number of customers for employees whose customers average credit limit > 90k.
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers 
    FROM employees e 
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber 
    GROUP BY e.employeeNumber 
    HAVING AVG(c.creditLimit) > 90000 
    ORDER BY num_customers DESC;
""", conn)

# STEP 7: Product name, count of orders (numorders), total quantity sold (totalunits). Sorted by totalunits DESC.
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(od.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits 
    FROM products p 
    JOIN orderdetails od ON p.productCode = od.productCode 
    GROUP BY p.productCode, p.productName 
    ORDER BY totalunits DESC;
""", conn)

# STEP 8: Product name, code, and total unique customers (numpurchasers). Sorted by numpurchasers DESC.
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers 
    FROM products p 
    JOIN orderdetails od ON p.productCode = od.productCode 
    JOIN orders o ON od.orderNumber = o.orderNumber 
    GROUP BY p.productCode, p.productName 
    ORDER BY numpurchasers DESC;
""", conn)

# STEP 9: Count of customers (n_customers), office code, and city per office.
df_customers = pd.read_sql("""
    SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city 
    FROM offices o 
    JOIN employees e ON o.officeCode = e.officeCode 
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber 
    GROUP BY o.officeCode, o.city;
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = None

conn.close()