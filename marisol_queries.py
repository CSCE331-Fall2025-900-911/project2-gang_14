import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="csce-315-db.engr.tamu.edu",
    database="gang_14_db",
    user="gang_14",
    password="gang_14",
)
cursor = conn.cursor()

#3 special query: peak day sales 
#tells us which day had the most revenue
cursor.execute("""
    SELECT 
        orders.order_date,
        SUM(orders.total_order_price) AS total_sales
    FROM orders 
    GROUP BY orders.order_date
    ORDER BY total_sales DESC
    LIMIT 10;
""")

#revenue by drink category
#tells us which drink category made the most money
cursor.execute("""
    SELECT 
        drink.product_type,
        SUM(order_drink.price) AS total_revenue
    FROM order_drink 
    JOIN drink ON order_drink.product_id = drink.product_id
    GROUP BY drink.product_type
    ORDER BY total_revenue DESC;
""")

#number of orders sorted by day of the week 
#tells us which days of the week were busiest
cursor.execute("""
    SELECT 
        TO_CHAR(orders.order_date, 'Day') AS day_of_week,
        COUNT(orders.order_id) AS num_orders
    FROM orders 
    GROUP BY day_of_week
    ORDER BY num_orders DESC;
""")
