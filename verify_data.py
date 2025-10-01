import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="csce-315-db.engr.tamu.edu",
    database="gang_14_db",
    user="gang_14",
    password="gang_14"
)
cursor = conn.cursor()

print("=== Verification Checks ===")

# Number of weeks of data
print("\n--- Weeks of Data ---")
cursor.execute("""
    SELECT COUNT(DISTINCT DATE_TRUNC('week', order_date)) AS total_weeks
    FROM orders;
""")
print(cursor.fetchone()[0])

# Total sales revenue
print("\n--- Total Sales Revenue ---")
cursor.execute("""
    SELECT ROUND(SUM(total_order_price)::numeric, 2) AS total_revenue
    FROM orders;
""")
print(cursor.fetchone()[0])

# Number of peak days
print("\n--- Number of Peak Days ---")
cursor.execute("""
    WITH daily_sales AS (
        SELECT DATE(order_date) AS day, SUM(total_order_price) AS sales
        FROM orders
        GROUP BY day
    ),
    avg_sales AS (
        SELECT AVG(sales) AS avg_daily_sales FROM daily_sales
    )
    SELECT COUNT(*) AS peak_days
    FROM daily_sales
    CROSS JOIN avg_sales
    WHERE daily_sales.sales > 2 * avg_sales.avg_daily_sales;
""")
print(cursor.fetchone()[0])

# Number of menu items
print("\n--- Number of Menu Items ---")
cursor.execute("""
    SELECT COUNT(DISTINCT product_name) FROM drink;
""")
print(cursor.fetchone()[0])

# Commit and close
conn.commit()
cursor.close()
conn.close()

