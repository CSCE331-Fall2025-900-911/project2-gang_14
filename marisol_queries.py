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
""")

#revenue by drink category over a specific date range
#tells us which drink category made the most money over a specified amount of time
cursor.execute("""
    SELECT 
        d.product_type,
        SUM(od.price) AS total_revenue,
        ROUND(100 * SUM(od.price)::numeric / SUM(SUM(od.price)) OVER ()::numeric, 2) AS percentage,
        RANK() OVER (ORDER BY SUM(od.price) DESC) AS category_rank
    FROM orders o
    JOIN order_drink od ON o.order_id = od.order_id
    JOIN drink d ON od.product_id = d.product_id
    WHERE o.order_date >= DATE '2025-08-01' -- Input starting date (start date of data- 2025-01-01)
    AND o.order_date < DATE '2025-09-01' -- Input ending date (end date of data: 2025-11-01)
    GROUP BY d.product_type
    ORDER BY category_rank;
""")

#number of orders sorted by day of the week per week
#tells us which days of the week were busiest by week number
cursor.execute("""
    SELECT 
        TO_CHAR(o.order_date, 'FMDay') AS day_of_week,
        COUNT(o.order_id) AS num_orders
    FROM orders o
    WHERE EXTRACT(WEEK FROM o.order_date) = 2   -- Change week number (1-40) here
    GROUP BY day_of_week
    ORDER BY num_orders DESC;
""")

# Commit and close
conn.commit()
cursor.close()
conn.close()

