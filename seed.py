import random
import datetime
import csv
import io

# -------------------------
# Static Data
# -------------------------

employees = [
    {"employee_id": 1, "employee_name": "John Smith", "employee_role" : "Manager"},
    {"employee_id": 2, "employee_name": "Jack Black", "employee_role" : "Cashier"},
    {"employee_id": 3, "employee_name": "Stacy Thomas", "employee_role" : "Cashier"},
    {"employee_id": 4, "employee_name": "Lizzy Murphy", "employee_role" : "Cashier"},
    {"employee_id": 5, "employee_name": "Alice Miller", "employee_role" : "Manager"}
]

ingredient_cost = {
    "Milk": 0.13,
    "Sugar Syrup": 0.08,
    "Matcha Powder": 0.25,
    "Water": 0,
    "Strawberry Syrup": 0.10,
    "Vanilla Ice Cream": 0.30,
    "Black Tapioca Pearls": 0.50,
    "Lychee Jelly": 0.20,
    "Mango Syrup": 0.10,
    "Black Milk Tea": 0.05,
    "Pudding": 0.12,
    "Berry Juice": 0.10,
    "Bursting Boba": 0.40,
    "Coconut Milk": 0.25,
    "Peach Jam": 0.10,
    "Lychee Juice": 0.18,
    "Green Tea": 0.05,
    "Honey Jelly": 0.12,
    "Thai Tea Mix": 0.30,
    "Oreo Cookies": 0.10,
    "Sweetened Condensed Milk": 0.13,
    "Cinnamon Syrup": 0.12,
    "Passion Fruit Jam": 0.10,
    "Mango Jam": 0.10,
    "Coffee": 0.55,
    "Taro Powder": 0.41,
    "Lemon Juice": 0.18,
    "Sparkling Water": 0.05,
    "Black Tea": 0.05,
    "Regular Pearl": 0.45,
    "Herb Jelly": 0.18,
    "Ice Cream": 0.35,
    "Mini Pearls": 0.40,
    "Aiyu Jelly": 0.22,
    "Creama": 0.25,
    "Crystal Boba": 0.38,
    "Mango Popping Boba": 0.42,
    "Strawberry Popping Boba": 0.42,
    "Coffee Jelly": 0.20,
    "Peach Popping Boba": 0.42,
    "Fresh Milk": 0.15
}

packaging_cost = {"cup": 0.15, "lid": 0.05, "straw": 0.05}

milk_tea_drink_to_ing = {
    "Classic Pearl Milk Tea": ["Black Tea", "Sugar Syrup", "Milk", "Black Tapioca Pearls"],
    "Thai Pearl Milk Tea": ["Thai Tea Mix", "Sweetened Condensed Milk", "Black Tapioca Pearls"],
    "Taro powder": ["Taro Powder", "Milk", "Sugar Syrup", "Black Tapioca Pearls"],
    "Golden Retriever": ["Black Milk Tea", "Pudding", "Coffee", "Lychee Jelly", "Black Tapioca Pearls"]
}

fruit_tea_drink_to_ing = {
    "Mango and Passion Fruit Tea": ["Green Tea", "Passion Fruit Jam", "Mango Jam"],
    "Berry Lychee Burs": ["Berry Juice", "Lychee Juice", "Bursting Boba"],
    "Peach Tea w/ Honey Jelly": ["Black Tea", "Peach Jam", "Honey Jelly"]
}

matcha_tea_drink_to_ing = {
    "Match Pearl Milk Tea": ["Milk", "Matcha Powder", "Water", "Sugar Syrup", "Black Tapioca Pearls"],
    "Mango Matcha Fresh Milk": ["Mango Syrup", "Milk", "Matcha Powder", "Water", "Sugar Syrup"],
    "Strawberry Matcha Fresh Milk": ["Strawberry Syrup", "Milk", "Matcha Powder", "Water", "Sugar Syrup"]
}

non_caffeinated_drink_to_ing = {
    "Tiger Boba": ["Black Tapioca Pearls", "Sugar Syrup", "Milk"],
    "Strawberry Coconut": ["Black Tapioca Pearls", "Strawberry Syrup", "Coconut Milk"],
    "Wintermelon Lemonade": ["Lemon Juice", "Sugar Syrup", "Cinnamon Syrup", "Sparkling Water"]
}

ice_blended_drink_to_ing = {
    "Strawberry ice Blended w/ Lychee Jelly and Ice Cream": ["Strawberry Syrup", "Vanilla Ice Cream", "Milk", "Lychee Jelly"],
    "Taro Ice Blended w/ Pudding": ["Taro Powder", "Milk", "Sugar Syrup"],
    "Oreo Ice Blended with pearl": ["Oreo Cookies", "Milk", "Vanilla Ice Cream", "Sugar Syrup"]
}

all_drinks = {
    "Milk Tea": milk_tea_drink_to_ing,
    "Fruit Tea": fruit_tea_drink_to_ing,
    "Matcha Tea": matcha_tea_drink_to_ing,
    "Non-Caffeinated": non_caffeinated_drink_to_ing,
    "Ice Blended": ice_blended_drink_to_ing
}

customizations = {
    "Ice Level": [1, 0.5, 0, 1.5],
    "Sweetness": [100, 80, 50, 30, 0, 120],
    "Toppings": [
        "Regular Pearl", "Lychee Jelly", "Pudding", "Herb Jelly", "Ice Cream",
        "Mini Pearls", "Aiyu Jelly", "Creama", "Crystal Boba", "Mango Popping Boba",
        "Strawberry Popping Boba", "Coffee Jelly", "Honey Jelly", "Peach Popping Boba", "Fresh Milk"
    ],
    "Miscellaneous": [
        "Double Topping", "Triple Topping", "Double Creama", "Split into two cups", "No toppings", "Sub pearls"
    ],
    "Temperature": [0, 1]
}

# -------------------------
# Config
# -------------------------

WEEKS = 40
TOTAL_REVENUE = 760000
START_DATE = datetime.datetime(2025, 1, 1)
PEAK_SALES_DATE = START_DATE + datetime.timedelta(weeks=20)
AVG_DRINK_PRICE = 7.5

# -------------------------
# Seeder
# -------------------------
def seed_data(cursor):
    # -------------------------
    # Insert employees
    # -------------------------
    print("Inserting employees...")
    for emp in employees:
        cursor.execute(
            "INSERT INTO employee (employee_id, employee_name, employee_role) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            (emp["employee_id"], emp["employee_name"], emp["employee_role"])
        )

    # -------------------------
    # Insert ingredients
    # -------------------------
    print("Inserting ingredients...")
    ingredient_map = {}
    all_ingredients = set(ingredient_cost.keys()) | set(packaging_cost.keys())
    for idx, name in enumerate(sorted(all_ingredients), start=1):
        if name in ingredient_cost:
            price = ingredient_cost[name]
        elif name in packaging_cost:
            price = packaging_cost[name]
        else:
            price = 0.00
        stock = random.randint(50, 500)
        cursor.execute(
            "INSERT INTO ingredient (ingredient_id, ingredient_name, stock, price) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;",
            (idx, name, stock, price)
        )
        ingredient_map[name] = idx

    # -------------------------
    # Insert customizations
    # -------------------------
    print("Inserting customizations...")
    for custom_id in range(1, 51):
        ice_level = random.choice(customizations["Ice Level"])
        sweetness = random.choice(customizations["Sweetness"])
        hot_cold = bool(random.choice(customizations["Temperature"]))
        num_toppings = random.randint(0, 3)
        selected_toppings = random.sample(customizations["Toppings"], min(num_toppings, len(customizations["Toppings"])))
        toppings_str = ", ".join(selected_toppings) if selected_toppings else None
        miscellaneous = random.choice([None, None, None] + customizations["Miscellaneous"])
        cursor.execute(
            "INSERT INTO customization (custom_id, ice_level, sweetness, hot_cold, toppings, miscellaneous) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
            (custom_id, ice_level, sweetness, hot_cold, toppings_str, miscellaneous)
        )
        for topping in selected_toppings:
            if topping in ingredient_map:
                cursor.execute(
                    "INSERT INTO customization_topping (custom_id, ingredient_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                    (custom_id, ingredient_map[topping])
                )

    # -------------------------
    # Prepare product templates
    # -------------------------
    print("Preparing product templates...")
    product_templates = []
    template_id = 1
    for product_type, drinks_dict in all_drinks.items():
        for drink, ings in drinks_dict.items():
            product_templates.append({
                "product_id": template_id,
                "product_name": drink,
                "product_type": product_type,
                "ingredients": ings
            })
            template_id += 1

    # -------------------------
    # Generate 500 pre-customized drinks
    # -------------------------
    print("Generating 500 pre-customized drinks...")
    precustomized_drinks = []
    drink_csv = io.StringIO()
    drink_ingredient_csv = io.StringIO()
    drink_id_counter = 1

    for _ in range(500):
        template = random.choice(product_templates)
        custom_id = random.randint(1, 50)
        base_price = 6.25
        packaging_price = 0.25
        topping_price = 0
        cursor.execute("SELECT toppings FROM customization WHERE custom_id=%s;", (custom_id,))
        toppings_result = cursor.fetchone()
        if toppings_result and toppings_result[0]:
            num_toppings = len(toppings_result[0].split(", "))
            topping_price = 0.75 * num_toppings
        price = base_price + packaging_price + topping_price

        precustomized_drinks.append({
            "product_id": drink_id_counter,
            "product_name": template['product_name'],
            "price": price,
            "product_type": template['product_type'],
            "custom_id": custom_id,
            "ingredients": template['ingredients']
        })

        drink_csv.write(f"{drink_id_counter}\t{template['product_name']}\t{price}\t{template['product_type']}\t{custom_id}\n")
        for ing in template['ingredients']:
            drink_ingredient_csv.write(f"{drink_id_counter}\t{ingredient_map[ing]}\t{random.randint(1, 2)}\n")

        drink_id_counter += 1

    # -------------------------
    # Generate orders
    # -------------------------
    print("Generating orders using pre-customized drinks...")
    orders_csv = io.StringIO()
    order_drinks_csv = io.StringIO()
    avg_revenue_per_week = TOTAL_REVENUE / WEEKS
    avg_transactions_per_week = int(avg_revenue_per_week / AVG_DRINK_PRICE)
    avg_transactions_per_day = avg_transactions_per_week // 7
    order_id = 1

    for week in range(WEEKS):
        week_start = START_DATE + datetime.timedelta(weeks=week)
        for _ in range(avg_transactions_per_week):
            num_drinks_in_order = random.randint(1, 3)
            order_drinks = random.sample(precustomized_drinks, num_drinks_in_order)
            emp = random.choice(employees)
            order_total = sum(d['price'] for d in order_drinks)
            day_offset = random.randint(0, 6)
            time_offset = random.randint(0, 86399)
            purchase_time = week_start + datetime.timedelta(days=day_offset, seconds=time_offset)
            orders_csv.write(f"{order_id}\t{emp['employee_id']}\t{order_total}\t{purchase_time.date()}\t{purchase_time.time()}\n")
            for d in order_drinks:
                order_drinks_csv.write(f"{order_id}\t{d['product_id']}\t{d['price']}\n")
            order_id += 1

    # Peak day double sales
    print(f"Adding double sales for peak day: {PEAK_SALES_DATE.date()}")
    for _ in range(avg_transactions_per_day * 2):
        num_drinks_in_order = random.randint(1, 3)
        order_drinks = random.sample(precustomized_drinks, num_drinks_in_order)
        emp = random.choice(employees)
        order_total = sum(d['price'] for d in order_drinks)
        time_offset = random.randint(0, 86399)
        purchase_time = PEAK_SALES_DATE + datetime.timedelta(seconds=time_offset)
        orders_csv.write(f"{order_id}\t{emp['employee_id']}\t{order_total}\t{purchase_time.date()}\t{purchase_time.time()}\n")
        for d in order_drinks:
            order_drinks_csv.write(f"{order_id}\t{d['product_id']}\t{d['price']}\n")
        order_id += 1

    # -------------------------
    # Bulk load
    # -------------------------
    # Bulk load drinks first
    print("Bulk loading drink records...")
    drink_csv.seek(0)
    cursor.copy_from(drink_csv, 'drink', columns=('product_id', 'product_name', 'price', 'product_type', 'custom_id'))

    print("Bulk loading drink_ingredient records...")
    drink_ingredient_csv.seek(0)
    cursor.copy_from(drink_ingredient_csv, 'drink_ingredient', columns=('product_id', 'ingredient_id', 'quantity'))

    # Then orders
    print(f"Bulk loading {order_id - 1} orders into database...")
    orders_csv.seek(0)
    cursor.copy_from(orders_csv, 'orders', columns=('order_id', 'employee_id', 'total_order_price', 'order_date', 'order_time'))

    print("Bulk loading order_drink records...")
    order_drinks_csv.seek(0)
    cursor.copy_from(order_drinks_csv, 'order_drink', columns=('order_id', 'product_id', 'price'))


    # -------------------------
    # Inventory
    # -------------------------
    print("Inserting inventory records...")

    # Get total stock and total asset from all ingredients
    cursor.execute("SELECT SUM(stock) FROM ingredient;")
    total_stock = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(price) FROM ingredient;")
    total_asset = (cursor.fetchone()[0] * total_stock) or 0

    cursor.execute("SELECT COUNT(*) FROM ingredient;")
    total_ingredients = cursor.fetchone()[0]
    inventory_id = 1
    cursor.execute(
        """
        INSERT INTO inventory (inventory_id, inventory_name, total_stock, total_asset)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
        """,
        (inventory_id, "sharetea_inventory", total_stock, total_asset)
    )
    sample_size = random.randint(10, min(25, total_ingredients))
    cursor.execute(
        "SELECT ingredient_id FROM ingredient ORDER BY RANDOM() LIMIT %s;",
        (sample_size,)
    )
    ingredient_ids = cursor.fetchall()

    for (ing_id,) in ingredient_ids:
        cursor.execute(
            """
            INSERT INTO inventory_ingredient (inventory_id, ingredient_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (inventory_id, ing_id)
        )
    print("Seeding complete!")