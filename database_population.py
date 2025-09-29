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

#Customization
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
    popularity_level FLOAT,
    custom_id INT,
    FOREIGN KEY (custom_id) REFERENCES customization(custom_id)
);
""")


#Ingredient
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredient (
    ingredient_id INT PRIMARY KEY,
    ingredient_name VARCHAR(255),
    stock INT,
    price FLOAT
);
""")

# Drink and Ingredient join table
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

# Order and Drink join table
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

# Inventory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT PRIMARY KEY,
    total_stock INT,
    total_asset FLOAT
);
""")

# Inventory and Ingredient join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory_ingredient (
    inventory_id INT,
    ingredient_id INT,
    PRIMARY KEY (inventory_id, ingredient_id),
    FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);
""")

# Customization and Ingredient join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customization_topping (
    custom_id INT,
    ingredient_id INT,
    PRIMARY KEY (custom_id, ingredient_id),
    FOREIGN KEY (custom_id) REFERENCES customization(custom_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);
""")

customizations = {
    "Ice Level" : [1, 0.5, 0, 1.5], #1 is regular ice
    "Sweetness" : [100, 80, 50, 30, 0, 120], #100 is regular sweetness
    "Toppings" : ["Regular Pearl", "Lychee Jelly", "Pudding", "Herb Jelly", "Ice Cream", "Mini Pearls", "Aiyu Jelly", 
                  "Creama", "Crystal Boba", "Mango Popping Boba", "Strawberry Popping Boba", "Coffee Jelly", "Honey Jelly", 
                  "Peach Popping Boba", "Fresh Milk"],
    "Miscellaneous" : ["Double Topping", "Triple Topping", "Double Creama", "Split into two cups", "No toppings", "Sub pearls"], 
    #if customer chooses another topping that is not pearl where pearls are included in the drink the select sub pearls
    "Temperature" : [0, 1] #0 is cold

}
milk_tea_drink_to_ing = {
    "Classic Pearl Milk Tea": ["Black Tea", "Sugar Syrup", "Milk", "Black Tapioca Pearls"],
    "Thai Pearl Milk Tea" : ["Thai Tea Mix", "Sweetened Condensed Milk" , "Black Tapioca Pearls"],
    "Taro powder" : ["Taro Powder", "Milk", "Sugar Syrup" , "Black Tapioca Pearls"],
    "Golden Retriever" : ["Black Milk Tea", "Pudding", "Coffee", "Lychee Jelly" , "Black Tapioca Pearls"]
}

fruit_tea_drink_to_ing = {
    "Mango and Passion Fruit Tea" : ["Green Tea", "Passion Fruit Jam", "Mango Jam"],
    "Berry Lychee Burs" : ["Berry Juice", "Lychee Juice", "Bursting Boba"],
    "Peach Tea w/ Honey Jelly" : ["Black Tea", "Peach Jam", "Honey Jelly"]
}

matcha_tea_drink_to_ing = {
    "Match Pearl Milk Tea" : ["Milk", "Matcha Powder", "Water", "Sugar Syrup", "Black Tapioca Pearls"], 
    "Mango Matcha Fresh Milk" : ["Mango Syrup", "Milk", "Matcha Powder", "Water", "Sugar Syrup"],
    "Strawberry Matcha Fresh Milk" : ["Strawberry Syrup", "Milk", "Matcha Powder", "Water", "Sugar Syrup" ] 
}


non_caffenited_drink_to_ing = {
    "Tiger Boba": ["Black Tapioca Pearls","Sugar Syrup","Milk"]
, "Strawberry Coconut": ["Black Tapioca Pearls","Strawberry Syrup","Coconut Milk",]
,"Wintermelon Lemonade": ["Lemon Juice","Sugar Syrup","Cinnamon Syrup","Sparkling Water"]
    
}
ice_blended_drink_to_ing = {
    "Strawberry ice Blended w/ Lychee Jelly and Ice Cream": ["Strawberry Syrup","Vanilla Ice Cream","Milk","Lychee Jelly"], 
    "Taro Ice Blended w/ Pudding": ["Taro Powder","Milk","Sugar Syrup",], 
    "Oreo Ice Blended with pearl": ["Oreo Cookies" ,"Milk","Vanilla Ice Cream","Sugar Syrup"]
}

ingredient_cost = {
    "Milk":0.13,
    "Sugar Syrup":0.08,
    "Matcha Powder":0.25,
    "Water":0,
    "Strawberry Syrup":0.10,
    "Vanilla Ice Cream":0.30,
    "Black Tapioca Pearls":0.5,
    "Lychee Jelly":0.20,
    "Mango Syrup":0.10,
    "Black Milk Tea":0.05,
    "Pudding":0.12,
    "Berry Juice":0.10,
    "Bursting Boba":0.40,
    "Coconut Milk":0.25,
    "Peach Jam":0.10,
    "Lychee Juice":0.18,
    "Green Tea":0.05, 
    "Honey Jelly":0.12,
    "Thai Tea Mix":0.30,  
    "Oreo Cookies":0.10,
    "Sweetened Condensed Milk":0.13,
    "Cinnamon Syrup":0.12,
    "Passion Fruit Jam":0.10,
    "Mango Jam":0.10,
    "Coffee":0.55,
    "Taro Powder":0.41,
    "Lemon Juice":0.18,
    "Sparkling Water":0.05
}

packaging_cost = {
    "cup" : 0.15,
    "lid" : 0.05,
    "straw" : 0.05
}

#employee details
employees= [
    {"employee_id":1,"employee_name":"John Smith"},
    {"employee_id":2,"employee_name":"Jack Black"},
    {"employee_id":3,"employee_name":"Stacy Thomas"},
    {"employee_id":4,"employee_name":"Lizzy Murphy"},
    {"employee_id":5,"employee_name":"Alice Miller"}
]



all_ingredients = set(ingredient_cost.keys())  
all_ingredients.update(customizations["Toppings"]) 
all_ingredients.update(packaging_cost.keys())

print(all_ingredients)

#insert ingredients into ingredient TABLE
ingredient_map = {}
for idx, name in enumerate(sorted(all_ingredients), start=1):
    if name in customizations["Toppings"]:
        price = 0.75 #fixed price of toppings
    elif name in ingredient_cost:
        price = ingredient_cost[name]
    elif name in packaging_cost:
        price = packaging_cost[name]
    else:
        price = 0.00
    stock = random.randint(10, 500)
    cursor.execute(
        """
        INSERT INTO ingredient (ingredient_id, ingredient_name, stock, price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        """,
        (idx, name, stock, price)
    )
    ingredient_map[name] = idx


for employee in employees:
    cursor.execute("""
                   Insert into employee(employee_id,employee_name) values (%s,%s,%s)
                   """,employee["employee_id"],employee["employee_name"])





# Commit and close
conn.commit()
cursor.close()
conn.close()

