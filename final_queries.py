import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="csce-315-db.engr.tamu.edu",
    database="gang_14_db",
    user="gang_14",
    password="gang_14",
)
cursor = conn.cursor()

# Helper function to run queries and print results
def run_query(cursor, query, title=""):
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"\n--- {title} ---")
    for row in rows:
        print(row)
    print("-" * 50)


# Siya's Queries


run_query(cursor, """
    SELECT EXTRACT(WEEK FROM order_date) AS week,
           COUNT(order_id) AS orders
    FROM orders
    GROUP BY week
    ORDER BY week;
""", title="Weekly Orders")

run_query(cursor, """
    SELECT e.employee_name,
           COUNT(o.order_id) AS orders
    FROM orders o
    JOIN employee e ON e.employee_id = o.employee_id
    GROUP BY e.employee_name
    ORDER BY orders DESC;
""", title="Total Sales by Employee")

run_query(cursor, """
    SELECT d.product_name,
           COUNT(DISTINCT di.ingredient_id) AS ingredients_in_a_drink
    FROM drink d
    JOIN drink_ingredient di ON d.product_id = di.product_id
    GROUP BY d.product_name
    ORDER BY d.product_name;
""", title="Ingredients Count per Drink")


# Marisol's Queries


run_query(cursor, """
   WITH ranked_orders AS (
        SELECT 
            o.order_id,
            o.order_date::date AS order_day,
            SUM(d.price) AS order_total,
            ROW_NUMBER() OVER (
                PARTITION BY o.order_date::date 
                ORDER BY SUM(d.price) DESC
            ) AS rank_in_day
        FROM orders o
        JOIN order_drink od ON o.order_id = od.order_id
        JOIN drink d ON od.product_id = d.product_id
        GROUP BY o.order_id, o.order_date::date
    )
    SELECT 
        order_day,
        SUM(order_total) AS top10_sales
    FROM ranked_orders
    WHERE rank_in_day <= 10
      AND order_day = DATE '2025-09-25'  -- Change date here
    GROUP BY order_day;
""", title="Top 10 Orders per Day")

run_query(cursor, """
    SELECT d.product_type,
           SUM(od.price) AS total_revenue,
           ROUND(100 * SUM(od.price)::numeric / SUM(SUM(od.price)) OVER ()::numeric, 2) AS percentage,
           RANK() OVER (ORDER BY SUM(od.price) DESC) AS category_rank
    FROM orders o
    JOIN order_drink od ON o.order_id = od.order_id
    JOIN drink d ON od.product_id = d.product_id
    WHERE o.order_date >= DATE '2025-08-01'
      AND o.order_date < DATE '2025-09-01'
    GROUP BY d.product_type
    ORDER BY category_rank;
""", title="Revenue by Drink Category")

run_query(cursor, """
    SELECT TO_CHAR(o.order_date, 'FMDay') AS day_of_week,
           COUNT(o.order_id) AS num_orders
    FROM orders o
    WHERE EXTRACT(WEEK FROM o.order_date) 
    GROUP BY day_of_week
    ORDER BY num_orders DESC;
""", title="Orders by Day of Week ")


# Renee's Queries


run_query(cursor, """
    SELECT i.ingredient_id,
           i.ingredient_name,
           COUNT(DISTINCT d.product_id) AS drink_count
    FROM ingredient i
    LEFT JOIN drink_ingredient d ON i.ingredient_id = d.ingredient_id
    GROUP BY i.ingredient_id, i.ingredient_name
    ORDER BY drink_count DESC, i.ingredient_name;
""", title="Total Drinks Using Each Ingredient")

run_query(cursor, """
    SELECT TO_CHAR(orders.order_date, 'Mon YYYY') AS month,
           COUNT(*) AS total_orders,
           SUM(total_order_price) AS total_revenue,
           ROUND(CAST(AVG(total_order_price) AS numeric), 2) AS avg_revenue
    FROM orders
    GROUP BY TO_CHAR(orders.order_date, 'Mon YYYY')
    ORDER BY TO_CHAR(orders.order_date, 'Mon YYYY');
""", title="Monthly Revenue Summary")

run_query(cursor, """
    SELECT TO_CHAR(orders.order_date, 'YYYY-MM') AS month,
           drink.product_name,
           COUNT(*) AS total_orders
    FROM orders
    JOIN order_drink ON orders.order_id = order_drink.order_id
    JOIN drink ON order_drink.product_id = drink.product_id
    GROUP BY month, drink.product_name
    ORDER BY month, total_orders DESC;
""", title="Most Popular Drinks per Month")


# Ananya's Queries


run_query(cursor, """
    SELECT TO_CHAR(o.order_time, 'HH24:00') AS order_hour,
           COUNT(DISTINCT o.order_id) AS num_orders,
           SUM(p.price) AS total_sales
    FROM orders o
    JOIN order_drink od ON o.order_id = od.order_id
    JOIN drink p ON od.product_id = p.product_id
    GROUP BY order_hour
    ORDER BY order_hour;
""", title="Orders per Hour")

run_query(cursor, """
    SELECT p.product_name,
           COUNT(*) AS times_ordered
    FROM order_drink od
    JOIN drink p ON od.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY times_ordered DESC
    LIMIT 5;
""", title="Top 5 Popular Drinks")

run_query(cursor, """
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
""", title="Most Expensive Orders")

# Close connection
cursor.close()
conn.close()
