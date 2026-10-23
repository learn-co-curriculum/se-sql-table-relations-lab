import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")

# Question 1: Find employees working in Boston
query1 = """
SELECT employees.*
FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
WHERE offices.city = 'Boston';
"""
print("\n1. Employees working in Boston:")
print(pd.read_sql(query1, conn))


# Question 2: Find offices that have no employees
query2 = """
SELECT offices.*
FROM offices
LEFT JOIN employees
ON offices.officeCode = employees.officeCode
WHERE employees.employeeNumber IS NULL;
"""
print("\n2. Offices with no employees:")
print(pd.read_sql(query2, conn))


# Question 3: List all employees with their office city and state
query3 = """
SELECT employees.firstName,
       employees.lastName,
       offices.city,
       offices.state
FROM employees
LEFT JOIN offices
ON employees.officeCode = offices.officeCode
ORDER BY employees.lastName, employees.firstName;
"""
print("\n3. Employees and their office locations:")
print(pd.read_sql(query3, conn))


# Question 4: Find customers who have never placed an order
query4 = """
SELECT customers.contactFirstName,
       customers.contactLastName,
       customers.phone,
       customers.salesRepEmployeeNumber
FROM customers
LEFT JOIN orders
ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY customers.contactLastName;
"""
print("\n4. Customers who have never placed an order:")
print(pd.read_sql(query4, conn))


# Question 5: List customer payments from highest to lowest
query5 = """
SELECT customers.customerName,
       payments.checkNumber,
       payments.amount
FROM customers
JOIN payments
ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
"""
print("\n5. Customer payments, highest to lowest:")
print(pd.read_sql(query5, conn))


# Question 6: Employees whose customers have an average credit limit over 90000
query6 = """
SELECT employees.employeeNumber,
       employees.firstName,
       employees.lastName,
       COUNT(customers.customerNumber) AS numberOfCustomers,
       AVG(customers.creditLimit) AS averageCreditLimit
FROM employees
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employees.employeeNumber,
         employees.firstName,
         employees.lastName
HAVING AVG(customers.creditLimit) > 90000
ORDER BY numberOfCustomers DESC;
"""
print("\n6. Employees whose customers have an average credit limit over 90000:")
print(pd.read_sql(query6, conn))


# Question 7: Count orders and units sold for each product
# Question 7: Count orders and units sold for each product
query7 = """
SELECT products.productCode,
       products.productName,
       COUNT(orderdetails.orderNumber) AS numorders,
       COALESCE(SUM(orderdetails.quantityOrdered), 0) AS totalunits
FROM products
LEFT JOIN orderdetails
ON products.productCode = orderdetails.productCode
GROUP BY products.productCode, products.productName
ORDER BY totalunits DESC;
"""

print("\n7. Products ranked by total units sold:")
print(pd.read_sql(query7, conn))

# Question 8: Count distinct customers who purchased each product
query8 = """
SELECT products.productCode,
       products.productName,
       COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products
LEFT JOIN orderdetails
ON products.productCode = orderdetails.productCode
LEFT JOIN orders
ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode, products.productName
ORDER BY numpurchasers DESC;
"""
print("\n8. Products ranked by number of customers who purchased them:")
print(pd.read_sql(query8, conn))


# Question 9: Count customers represented by each office
query9 = """
SELECT offices.officeCode,
       offices.city,
       COUNT(DISTINCT customers.customerNumber) AS n_customers
FROM offices
LEFT JOIN employees
ON offices.officeCode = employees.officeCode
LEFT JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode, offices.city
ORDER BY n_customers DESC;
"""
print("\n9. Number of customers represented by each office:")
print(pd.read_sql(query9, conn))


# Question 10: Find employees associated with customers who ordered products
# purchased by fewer than 20 distinct customers
# Question 10: Find employees associated with customers who ordered products
# purchased by fewer than 20 distinct customers

query10 = """
SELECT DISTINCT employees.employeeNumber,
       employees.firstName,
       employees.lastName,
       offices.city,
       offices.officeCode
FROM employees
JOIN offices
ON employees.officeCode = offices.officeCode
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders
ON customers.customerNumber = orders.customerNumber
JOIN orderdetails
ON orders.orderNumber = orderdetails.orderNumber
WHERE orderdetails.productCode IN (
    SELECT orderdetails.productCode
    FROM orderdetails
    JOIN orders
    ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY orderdetails.productCode
    HAVING COUNT(DISTINCT orders.customerNumber) < 20
)
ORDER BY employees.employeeNumber;
"""

print("\n10. Employees associated with qualifying products:")
print(pd.read_sql(query10, conn))

conn.close()
