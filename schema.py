def drop_schema(cursor):
    cursor.execute("""
    DROP TABLE IF EXISTS order_drink CASCADE;
    DROP TABLE IF EXISTS orders CASCADE;
    DROP TABLE IF EXISTS employee CASCADE;
    DROP TABLE IF EXISTS drink_ingredient CASCADE;
    DROP TABLE IF EXISTS drink CASCADE;
    DROP TABLE IF EXISTS customization_topping CASCADE;
    DROP TABLE IF EXISTS customization CASCADE;
    DROP TABLE IF EXISTS inventory_ingredient CASCADE;
    DROP TABLE IF EXISTS inventory CASCADE;
    DROP TABLE IF EXISTS ingredient CASCADE;
    """)

def create_schema(cursor):
    # Customization
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customization (
        custom_id INT PRIMARY KEY,
        ice_level FLOAT,
        sweetness INT,
        hot_cold BOOLEAN,
        toppings VARCHAR(255),
        miscellaneous VARCHAR(255)
    );
    """)

    # Drink
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drink (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(255),
        price FLOAT,
        product_type VARCHAR(255),
        custom_id INT,
        FOREIGN KEY (custom_id) REFERENCES customization(custom_id)
    );
    """)

    # Ingredient
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredient (
        ingredient_id INT PRIMARY KEY,
        ingredient_name VARCHAR(255),
        stock INT,
        price FLOAT
    );
    """)

    # Drink and Ingredient join
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drink_ingredient (
        product_id INT,
        ingredient_id INT,
        quantity FLOAT,
        PRIMARY KEY (product_id, ingredient_id),
        FOREIGN KEY (product_id) REFERENCES drink(product_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
    );
    """)

    # Employee
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee (
        employee_id INT PRIMARY KEY,
        employee_name VARCHAR(255),
        employee_role VARCHAR(255)
    );
    """)

    # Orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        employee_id INT,
        total_order_price FLOAT,
        order_date DATE,
        order_time TIME,
        FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
    );
    """)

    # Order and Drink join
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_drink (
        order_id INT,
        product_id INT,
        price FLOAT,
        PRIMARY KEY (order_id, product_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES drink(product_id)
    );
    """)

    # Inventory
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT PRIMARY KEY,
    inventory_name VARCHAR(255),
    total_stock INT DEFAULT 0,
    total_asset FLOAT DEFAULT 0
    );
    """)



    # Customization + Topping join
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customization_topping (
        custom_id INT,
        ingredient_id INT,
        PRIMARY KEY (custom_id, ingredient_id),
        FOREIGN KEY (custom_id) REFERENCES customization(custom_id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
    );
    """)
    

import psycopg2   
conn = psycopg2.connect(
    host="csce-315-db.engr.tamu.edu",
    database="gang_14_db",
    user="gang_14",
    password="gang_14",
)
cursor = conn.cursor()
drop_schema(cursor)
create_schema(cursor)
conn.commit()
cursor.close()
conn.close()


