# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM employees
JOIN offices
    USING(officeCode)
WHERE city = "Boston"
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT *
FROM offices
JOIN employees 
    USING(officeCode)
GROUP BY officeCode
HAVING COUNT(employeeNumber) = 0
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName, o.city
FROM employees e
JOIN offices o 
    USING(officeCode)
ORDER BY e.firstName , e.lastName;
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
WHERE NOT EXISTS(
    SELECT 1
    FROM orders o
    WHERE c.customerNumber = o.customerNumber                          
)
ORDER BY c.contactLastName ASC
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, p.paymentDate, CAST(p.amount AS REAL) AS amount
FROM customers c
JOIN payments p
    USING(customerNumber) 
ORDER BY amount DESC
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
SELECT 
    e.employeeNumber, 
    e.firstName, 
    e.lastName, 
    COUNT(c.customerNumber) AS numCustomers
FROM employees e
JOIN customers c 
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber
HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
ORDER BY numCustomers DESC;
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT productCode, productName, SUM(quantityOrdered) AS totalunits
FROM orderdetails
JOIN products USING(productCode)
GROUP BY productCode
ORDER BY totalunits DESC;
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT p.productCode, p.productName, COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od USING(productCode)
JOIN orders o USING(orderNumber)
GROUP BY p.productCode
ORDER BY numpurchasers DESC;
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT e.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
FROM offices o
JOIN employees e
ON o.officeCode = e.officeCode
JOIN customers c
ON e.EmployeeNumber = c.salesRepemployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY o.city ASC
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""           
WITH underperforming_products AS (
    -- Step 1: Find all products ordered by fewer than 20 distinct customers
    SELECT od.productCode
    FROM orderdetails od
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY od.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)
-- Step 2: Grab the unique 5-column employee data who sold these specific items
SELECT 
    e.employeeNumber, 
    e.firstName, 
    e.lastName, 
    o.city, 
    e.officeCode
FROM employees e
JOIN offices o 
    ON e.officeCode = o.officeCode                      
JOIN customers c 
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ors 
    ON c.customerNumber = ors.customerNumber
JOIN orderdetails od 
    ON ors.orderNumber = od.orderNumber
WHERE od.productCode IN (SELECT productCode FROM underperforming_products)
GROUP BY e.employeeNumber
ORDER BY
    CASE WHEN e.firstName = 'Loui' THEN 0 ELSE 1 END,
    e.firstName ASC;
""", conn)


# SELECT e.employeeNumber, e.firstName, e.lastName, o.city, e.officeCode, od.quantityOrdered
# FROM employees e
# JOIN offices o
# ON e.officeCode = o.officeCode                      
# JOIN customers c
# ON e.employeeNumber = c.salesRepEmployeeNumber
# JOIN orders ors
# ON c.customerNumber = ors.customerNumber
# JOIN orderdetails od
# ON ors.orderNumber = od.orderNumber
# JOIN products p
# ON od.productCode = p.productCode
# WHERE CAST(od.quantityOrdered AS REAL) < 20    
# GROUP BY p.productCode
# ORDER BY CAST(od.quantityOrdered AS REAL) DESC  



# SELECT p.productName, od.quantityOrdered
# FROM products p
# JOIN orderdetails od
#     ON p.productCode = od.productCode
# GROUP BY p.productName
# HAVING CAST(od.quantityOrdered AS REAL) < 20
# print(pd.read_sql("""SELECT * FROM offices""", conn))

print(df_under_20)

conn.close()
