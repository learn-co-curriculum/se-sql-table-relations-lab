# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

df_boston = pd.read_sql("""
SELECT
    e.firstName,
    e.lastName
FROM employees e
JOIN offices o
ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
""", conn)

# STEP 2
df_zero_emp = pd.read_sql("""
SELECT o.officeCode,
       o.city
FROM offices o
LEFT JOIN employees e
ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL
ORDER BY
e.firstName ASC
""", conn)

# STEP 3
df_employee = pd.read_sql("""
SELECT e.firstName,
       e.lastName,
       o.city,
       o.state
FROM employees e
LEFT JOIN offices o
ON e.officeCode = o.officeCode
ORDER BY e.firstName,
         e.lastName
""", conn)

# STEP 4
df_contacts = pd.read_sql("""
SELECT
    c.contactFirstName,
    c.contactLastName,
    c.phone,
    c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o
ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
""", conn)

# STEP 5
df_payment = pd.read_sql("""
SELECT
    c.contactFirstName,
    c.contactLastName,
    p.amount,
    p.paymentDate
FROM payments p
JOIN customers c
ON p.customerNumber = c.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

# STEP 6
df_credit = pd.read_sql("""
SELECT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    COUNT(c.customerNumber) AS numcustomers
FROM employees e
JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber
HAVING AVG(c.creditLimit) > 90000
ORDER BY numcustomers DESC
""", conn)

# STEP 7
df_product_sold = pd.read_sql("""
SELECT
    p.productName,
    COUNT(od.orderNumber) AS numorders,
    SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
GROUP BY p.productCode
ORDER BY totalunits DESC
""", conn)

# STEP 8
df_total_customers = pd.read_sql("""
SELECT
    p.productName,
    p.productCode,
    COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
JOIN orders o
ON od.orderNumber = o.orderNumber
GROUP BY p.productCode
ORDER BY numpurchasers DESC
""", conn)

# STEP 9
df_customers = pd.read_sql("""
SELECT
    o.officeCode,
    o.city,
    COUNT(c.customerNumber) AS n_customers
FROM offices o
LEFT JOIN employees e
ON o.officeCode = e.officeCode
LEFT JOIN customers c
ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode
""", conn)

# STEP 10
df_under_20 = pd.read_sql("""
SELECT DISTINCT
    e.employeeNumber,
    e.firstName,
    e.lastName,
    o.city,
    o.officeCode
FROM employees e
JOIN offices o
    ON e.officeCode = o.officeCode
JOIN customers c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord
    ON c.customerNumber = ord.customerNumber
JOIN orderdetails od
    ON ord.orderNumber = od.orderNumber
JOIN (
    SELECT
        od.productCode
    FROM orderdetails od
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY od.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
) under20
    ON od.productCode = under20.productCode
ORDER BY
    e.lastName,
    e.firstName
""", conn)

conn.close()
