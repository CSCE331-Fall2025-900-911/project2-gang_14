#write queries here

import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="csce-315-db.engr.tamu.edu",
    database="gang_14_db",
    user="gang_14",
    password="gang_14",
)
cursor = conn.cursor()

#2 special query: realistic sales history
cursor.execute("""
    SELECT 
    TO_CHAR(o.order_time, 'HH24:00') AS order_hour,
    COUNT(DISTINCT o.order_id) AS num_orders,
    SUM(p.price) AS total_sales
    FROM orders o
    JOIN order_drink od ON o.order_id = od.order_id
    JOIN drink p ON od.product_id = p.product_id
    GROUP BY order_hour
    ORDER BY order_hour;
""")

#query 2: gets popular drinks (top 5)
cursor.execute("""
    SELECT 
    p.product_name,
    COUNT(*) AS times_ordered
    FROM order_drink od
    JOIN drink p ON od.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY times_ordered DESC
    LIMIT 5;
 
""") 
#query 3: most expensive orders where order_total is distinct 
cursor.execute("""
    SELECT DISTINCT ON (order_total)
    o.order_id,
    SUM(p.price) AS order_total,
    STRING_AGG(p.product_name, ', ' ORDER BY p.product_name) AS drinks
    FROM orders o
    JOIN order_drink od ON o.order_id = od.order_id
    JOIN drink p ON od.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY order_total DESC
    LIMIT 5;
""") 


# Commit and close
conn.commit()
cursor.close()
conn.close()

