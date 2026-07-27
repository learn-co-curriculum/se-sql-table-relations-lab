# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# View schema (optional - for reference)
print("Database Schema:")
print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))

# ==================== PART 1: Join and Filter ====================
print("\n" + "="*50)
print("PART 1: Join and Filter")
print("="*50)

# Question 1: Employees in Boston
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
result1 = pd.read_sql(query1, conn)
print(result1)

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
result2 = pd.read_sql(query2, conn)
print(result2)

# ==================== PART 2: Type of Join ====================
print("\n" + "="*50)
print("PART 2: Type of Join")
print("="*50)

# Question 1: All employees with office location
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
result3 = pd.read_sql(query3, conn)
print(result3)

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
result4 = pd.read_sql(query4, conn)
print(result4)

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
result5 = pd.read_sql(query5, conn)
print(result5)

# ==================== PART 4: Joining and Grouping ====================
print("\n" + "="*50)
print("PART 4: Joining and Grouping")
print("="*50)

# Question 1: Top employees with high average credit limits
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
result6 = pd.read_sql(query6, conn)
print(result6)

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
result7 = pd.read_sql(query7, conn)
print(result7)

# ==================== PART 5: Multiple Joins ====================
print("\n" + "="*50)
print("PART 5: Multiple Joins")
print("="*50)

# Question 1: Product purchasers count
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
result8 = pd.read_sql(query8, conn)
print(result8)

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
result9 = pd.read_sql(query9, conn)
print(result9)

# ==================== PART 6: Subquery ====================
print("\n" + "="*50)
print("PART 6: Subquery")
print("="*50)

# Employees who sold products with fewer than 20 customers
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
result10 = pd.read_sql(query10, conn)
print(result10)

# ==================== Close Connection ====================
conn.close()
print("\nDatabase connection closed.")