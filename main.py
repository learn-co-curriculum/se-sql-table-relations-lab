# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM employees 
JOIN offices ON employees.officeCode = offices.officeCode
WHERE offices.city = 'Boston';
""", conn)

#print(df_boston)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT *
FROM offices
LEFT JOIN employees ON offices.officeCode = employees.officeCode
WHERE employees.employeeNumber is NULL;
""", conn)

#print(df_zero_emp)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT firstName, lastName, city, state
FROM employees 
LEFT JOIN offices ON employees.officeCode = offices.officeCode
ORDER BY employees.firstName, employees.lastName;
""", conn)

#print(df_employee)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers
LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY customers.contactLastName;
""", conn)

#print(df_contacts)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT contactFirstName, contactLastName, amount, paymentDate
FROM customers
JOIN payments ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
""", conn)

#print(df_payment)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
SELECT employees.employeeNumber, employees.firstName, employees.lastName, COUNT(customers.customerNumber) as total_customers
FROM employees
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employees.employeeNumber, employees.firstName, employees.lastName
HAVING AVG(customers.creditLimit) > 90000
ORDER BY total_customers DESC;
""", conn)

#print(df_credit)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT productName, COUNT(orderNumber) AS num_ordered,
SUM(quantityOrdered) AS totalunits
FROM products
JOIN orderDetails ON products.productCode = orderDetails.productCode
GROUP BY productName
ORDER BY totalunits DESC;
""", conn)

#print(df_product_sold)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT products.productName, products.productCode, COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products 
JOIN orderDetails ON products.productCode = orderDetails.productCode
JOIN orders ON orderDetails.orderNumber = orders.orderNumber
GROUP BY products.productName, products.productCode 
ORDER BY numpurchasers DESC;
""", conn)

#print(df_total_customers)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT offices.officeCode, offices.city, COUNT(customers.customerNumber) AS n_customers
FROM offices
JOIN employees ON offices.officeCode = employees.officeCode
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode, offices.city;
""", conn)

#print(df_customers)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.officeCode
FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders ON customers.customerNumber = orders.customerNumber
JOIN orderDetails ON orders.orderNumber = orderDetails.orderNumber
WHERE orderDetails.productCode IN (
    SELECT products.productCode
    FROM products
    JOIN orderDetails ON products.productCode = orderDetails.productCode
    JOIN orders ON orderDetails.orderNumber = orders.orderNumber
    GROUP BY products.productCode
    HAVING COUNT(DISTINCT orders.customerNumber) < 20 )
ORDER BY employees.lastName, employees.firstName;
""", conn)

print(df_under_20)

conn.close()