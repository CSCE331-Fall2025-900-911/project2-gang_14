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

cursor.execute("""
    SELECT 
        EXTRACT(WEEK FROM order_date) AS week,
        COUNT(order_id) AS orders
    FROM orders
    GROUP BY week
    ORDER BY week;
""") #extract week in postgreSQL and count the total orders

