#write queries here

import psycopg2
import random

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="csce-315-db.engr.tamu.edu",
    database="gang_14_db",
    user="gang_14",
    password="gang_14",
)
cursor = conn.cursor()
#extract week in postgreSQL and count the total orders
cursor.execute("""
    SELECT 
        EXTRACT(WEEK FROM order_date) AS week,
        COUNT(order_id) AS orders
    FROM orders
    GROUP BY week
    ORDER BY week;
""") 

#Display total sales grouped by each employee 
cursor.execute("""
    SELECT 
        employee_name as employee_name ,
        COUNT(order_id) AS orders
    FROM orders o
    join employee e on e.employee_id = o.employee_id
    GROUP BY e.employee_name
    ORDER BY orders DESC;
    ;
""") 

# count the number of ingredients in a drink
cursor.execute("""
    SELECT 
    d.product_name,
    COUNT(DISTINCT di.ingredient_id) AS ingredients_in_a_drink
    FROM drink d
    JOIN drink_ingredient di
    ON d.product_id = di.product_id
    GROUP BY d.product_name
    ORDER BY d.product_name;
    ;
""") 


