# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# ==================== PART 1: Join and Filter ====================
print("\n" + "="*50)
print("PART 1: Join and Filter")
print("="*50)

# Question 1: Employees in Boston - MUST be named df_boston
print("\nEmployees in Boston:")
query1 = """
SELECT 
    e.firstName,
    e.lastName,
    e.jobTitle
FROM employees e
INNER JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
"""
df_boston = pd.read_sql(query1, conn)  # ← MUST be named df_boston
print(df_boston)

# Question 2: Offices with zero employees
print("\nOffices with zero employees:")
query2 = """
SELECT 
    o.officeCode,
    o.city,
    COUNT(e.employeeNumber) as employee_count
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
GROUP BY o.officeCode, o.city
HAVING COUNT(e.employeeNumber) = 0;
"""
df_zero_offices = pd.read_sql(query2, conn)  # ← Can be any name
print(df_zero_offices)

# ==================== PART 2: Type of Join ====================
print("\n" + "="*50)
print("PART 2: Type of Join")
print("="*50)

# Question 1: All employees with office location - MUST be named df_employee
print("\nAll employees with office location:")
query3 = """
SELECT 
    e.firstName,
    e.lastName,
    o.city,
    o.state
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName;
"""
df_employee = pd.read_sql(query3, conn)  # ← MUST be named df_employee
print(df_employee)

# Question 2: Customers who haven't placed orders
print("\nCustomers who haven't placed orders:")
query4 = """
SELECT 
    c.contactFirstName,
    c.contactLastName,
    c.phone,
    c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName;
"""
df_no_orders = pd.read_sql(query4, conn)  # ← Can be any name
print(df_no_orders)

# ==================== PART 3: Built-In Function ====================
print("\n" + "="*50)
print("PART 3: Built-In Function")
print("="*50)

# Payments report with amount sorting
print("\nPayments report:")
query5 = """
SELECT 
    c.contactFirstName,
    c.contactLastName,
    p.amount,
    p.paymentDate
FROM customers c
INNER JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
"""
df_payments = pd.read_sql(query5, conn)  # ← Can be any name
print(df_payments)

# ==================== PART 4: Joining and Grouping ====================
print("\n" + "="*50)
print("PART 4: Joining and Grouping")
print("="*50)

# Question 1: Top employees with high average credit limits - MUST be named df_credit
print("\nTop employees with high average credit limits:")
query6 = """
SELECT 
    e.employeeNumber,
    e.firstName,
    e.lastName,
    COUNT(c.customerNumber) as num_customers
FROM employees e
INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_customers DESC
LIMIT 4;
"""
df_credit = pd.read_sql(query6, conn)  # ← MUST be named df_credit
print(df_credit)

# Question 2: Product sales analysis
print("\nProduct sales analysis:")
query7 = """
SELECT 
    p.productName,
    COUNT(od.orderNumber) as numorders,
    SUM(od.quantityOrdered) as totalunits
FROM products p
INNER JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productName
ORDER BY totalunits DESC;
"""
df_product_sales = pd.read_sql(query7, conn)  # ← Can be any name
print(df_product_sales)

# ==================== PART 5: Multiple Joins ====================
print("\n" + "="*50)
print("PART 5: Multiple Joins")
print("="*50)

# Question 1: Product purchasers count - MUST be named df_total_customers
print("\nProduct purchasers count:")
query8 = """
SELECT 
    p.productName,
    p.productCode,
    COUNT(DISTINCT o.customerNumber) as numpurchasers
FROM products p
INNER JOIN orderdetails od ON p.productCode = od.productCode
INNER JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productName, p.productCode
ORDER BY numpurchasers DESC;
"""
df_total_customers = pd.read_sql(query8, conn)  # ← MUST be named df_total_customers
print(df_total_customers)

# Question 2: Customers per office
print("\nCustomers per office:")
query9 = """
SELECT 
    o.officeCode,
    o.city,
    COUNT(DISTINCT c.customerNumber) as n_customers
FROM offices o
INNER JOIN employees e ON o.officeCode = e.officeCode
INNER JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY n_customers DESC;
"""
df_customers_per_office = pd.read_sql(query9, conn)  # ← Can be any name
print(df_customers_per_office)

# ==================== PART 6: Subquery ====================
print("\n" + "="*50)
print("PART 6: Subquery")
print("="*50)

# Employees who sold products with fewer than 20 customers - MUST be named df_under_20
print("\nEmployees who sold products with fewer than 20 customers:")
query10 = """
SELECT 
    e.employeeNumber,
    e.firstName,
    e.lastName,
    o.city,
    o.officeCode
FROM employees e
INNER JOIN offices o ON e.officeCode = o.officeCode
WHERE e.employeeNumber IN (
    SELECT DISTINCT c.salesRepEmployeeNumber
    FROM customers c
    INNER JOIN orders ord ON c.customerNumber = ord.customerNumber
    INNER JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT p.productCode
        FROM products p
        INNER JOIN orderdetails od2 ON p.productCode = od2.productCode
        INNER JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
        GROUP BY p.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
)
ORDER BY e.employeeNumber;
"""
df_under_20 = pd.read_sql(query10, conn)  # ← MUST be named df_under_20
print(df_under_20)

# ==================== Close Connection ====================
conn.close()
print("\nDatabase connection closed.")