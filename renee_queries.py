import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="csce-315-db.engr.tamu.edu",
    database="gang_14_db",
    user="gang_14",
    password="gang_14",
)
cursor = conn.cursor()

#query 1: Total drinks that use an ingredient
cursor.execute("""
    SELECT
        i.ingredient_id,
        i.ingredient_name,
        COUNT(DISTINCT d.product_id) AS drink_count
    FROM ingredient i
    LEFT JOIN drink_ingredient d ON i.ingredient_id = d.ingredient_id
    GROUP BY i.ingredient_id, i.ingredient_name
    ORDER BY drink_count DESC, i.ingredient_name;
""")

#query 2: gets total orders, total revenue and average revenue per month
cursor.execute("""
    SELECT
        TO_CHAR(orders.order_date, 'Mon YYYY') AS month,
        COUNT(*) AS total_orders,
        SUM(total_order_price) AS total_revenue,
        ROUND(CAST(AVG(total_order_price) AS numeric), 2) AS avg_revenue
    FROM orders
    GROUP BY month
    ORDER BY month;
 
""") 
#query 3: Sorted by most popular drink to least popular drink per month
cursor.execute("""
    SELECT
        TO_CHAR(orders.order_date, 'YYYY-MM') AS month,
        drink.product_name,
        COUNT(*) AS total_orders
    FROM orders
    JOIN order_drink ON orders.order_id = order_drink.order_id
    JOIN drink ON order_drink.product_id = drink.product_id
    GROUP BY month, drink.product_name
    ORDER BY month, total_orders DESC;
""") 


# Commit and close
conn.commit()
cursor.close()
conn.close()