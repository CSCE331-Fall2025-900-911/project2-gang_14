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

# Customization
cursor.execute("""
CREATE TABLE IF NOT EXISTS customization (
    custom_id INT PRIMARY KEY,
    type VARCHAR(255),
    option_name VARCHAR(255),
    extra_cost FLOAT
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

customization =[
    [1,"Ice Level", "1", 0.0],
    [2,"Ice Level", "0.5", 0.0],
    [3,"Ice Level", "0", 0.0],
    [4,"Ice Level", "1.5", 0.0],

    [5,"Sweetness", "100", 0.0],
    [6,"Sweetness", "80", 0.0],
    [7,"Sweetness", "50", 0.0],
    [8,"Sweetness", "30", 0.0],
    [9,"Sweetness", "0", 0.0],
    [10,"Sweetness", "120", 0.0],

    [12,"Toppings", "Regular Pearl", 0.5],
    [13,"Toppings", "Lychee Jelly", 0.5],
    [14,"Toppings", "Pudding", 0.5],
   
    [15,"Toppings", "Ice Cream", 0.5],
    [16,"Toppings", "Mini Pearls", 0.5],
    [17,"Toppings", "Aiyu Jelly", 0.5],
    [18,"Toppings", "Creama", 0.5],
    [19,"Toppings", "Crystal Boba", 0.5],
    [20,"Toppings", "Mango Popping Boba", 0.5],
    [21,"Toppings", "Strawberry Popping Boba", 0.5],
    [22,"Toppings", "Coffee Jelly", 0.5],
    [23,"Toppings", "Honey Jelly", 0.5],
    [24,"Toppings", "Peach Popping Boba", 0.5],
    [25,"Toppings", "Fresh Milk", 0.5],

    [26,"Miscellaneous", "Double Topping", 0.25],
    [27,"Miscellaneous", "Triple Topping", 0.25],
    [28,"Miscellaneous", "Double Creama", 0.25],
    [29,"Miscellaneous", "Split into two cups", 0.25],
    [30,"Miscellaneous", "No toppings", 0.25],
    [31,"Miscellaneous", "Sub pearls", 0.25],
  
    [32,"Temperature", "0", 0.0], 
    [33,"Temperature", "1", 0.0]   
]
for custom_items in customization:
    cursor.execute(
        """
        insert into customization(custom_id,type,option_name,extra_cost) VALUES (%s, %s, %s, %s);
        """,(custom_items[0],custom_items[1],custom_items[2],custom_items[3])
    )



# Drink 
cursor.execute("""
CREATE TABLE IF NOT EXISTS drink (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price FLOAT,
    product_type VARCHAR(255)
);
""")
products =[
    [1,"Classic Pearl Milk Tea", 5.80, "Milk Tea"],
    [2,"Thai Pearl Milk Tea ", 6.25, "Milk Tea"],
    [3,"Taro Pearl Milk Tea", 6.25, "Milk Tea"],
    [4,"Golden Retriever", 6.75, "Milk Tea"],

    [5,"Mango and Passion Fruit Tea", 6.25, "Fruit Tea"],
    [6,"Berry Lychee Burst", 6.25, "Fruit Tea"],
    [7,"Peach Tea w/ Honey Jelly", 6.25, "Fruit Tea"],
    
    
    [8,"Match Pearl Milk Tea", 6.50, "Matcha"],
    [9,"Mango Matcha Fresh Milk", 6.50, "Matcha"],
    [10,"Strawberry Matcha Fresh Milk", 6.50, "Matcha"],

    [11,"Tiger Boba", 6.50, "Non-Caffenited"],
    [12,"Strawberry Coconut", 6.50, "Non-Caffenited"],
    [13,"Wintermelon Lemonade", 6.50, "Non-Caffenited"],
    
    
    [14,"Strawberry ice Blended w/ Lychee Jelly and Ice Cream", 6.75, "Ice Blended"],
    [15,"Taro Ice Blended w/ Pudding", 6.75, "Ice Blended"],
    [16,"Oreo Ice Blended with pearl", 6.75, "Ice Blended"]
   
]
for product in products:
    cursor.execute(
        """
        insert into drink(product_id, product_name, price, product_type) 
        VALUES (%s, %s, %s, %s);
        """, (product[0], product[1], product[2], product[3])
    )
        

# Ingredient
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredient (
    ingredient_id INT PRIMARY KEY,
    ingredient_name VARCHAR(255),
    unit VARCHAR(255),
    stock INT,
    cost_per_unit FLOAT,
    reorder_threshold INT
);
""")



# Drink and Ingredient join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS drink_ingredient (
    product_id INT,
    ingredient_id INT,
    quantity_needed FLOAT,
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
    role VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255)
);
""")
#employee details
employees= [
    {"employee_id":1,"employee_name":"John Smith","role":"Cashier","username":"John_Smith","password":"HiMyNameIsJohn"},
    {"employee_id":2,"employee_name":"Jack Black","role":"Manager","username":"Jack_Black","password":"HiMyNameIsJack"},
    {"employee_id":3,"employee_name":"Stacy Thomas","role":"Barista","username":"Stacy_Thomas","password":"HiMyNameIsStacy"},
    {"employee_id":4,"employee_name":"Lizzy Murphy","role":"Cleaner","username":"Lizzy_Murphy","password":"HiMyNameIsLizzy"},
    {"employee_id":5,"employee_name":"Alice Miller","role":"Owner","username":"Alice_Miller","password":"HiMyNameIsAlice"}
]
for employee in employees:
    cursor.execute("""
                   Insert into employee(employee_id,employee_name,role,username,password) values (%s,%s,%s,%s,%s)
                   """,employee["employee_id"],employee["employee_name"],employees["role"],employees["username"],employees["password"])


# Orders 
cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_order (
    order_id INT PRIMARY KEY,
    order_time TIMESTAMP,
    employee_id INT,
    total_price FLOAT,

);
""")

# Order and Drink join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_drink (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity FLOAT,
    price FLOAT,
    FOREIGN KEY (order_id) REFERENCES customer_order(order_id),
    FOREIGN KEY (product_id) REFERENCES drink(product_id)
);
""")
# Order and Customization join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_customization (
    order_item_id INT ,
    customization_id INT,
    PRIMARY KEY (order_item_id, customization_id),
    FOREIGN KEY (order_item_id) REFERENCES order_drink(order_item_id),
    FOREIGN KEY (customization_id) REFERENCES customization(customization_id)
    
);
""")



# Customization and Ingredient join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customization_topping (
    custom_id INT,
    ingredient_id INT,
    quantity_needed VARCHAR(255),
    PRIMARY KEY (custom_id, ingredient_id),
    FOREIGN KEY (custom_id) REFERENCES customization(custom_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);
""")


#Menu Items with their ingredients
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
    reorder_threshold = random.randint(500,100)
    unit = "unit"
    cursor.execute(
        """
        INSERT INTO ingredient (ingredient_id, ingredient_name,unit, stock, cost_price_unit,reorder_threshold)
        VALUES (%s, %s, %s, %s,%s)
        ON CONFLICT DO NOTHING
        """,
        (idx, name, unit, stock, price,reorder_threshold)
    )
    ingredient_map[name] = idx


#populate DrinkIngridient Table for which ingrideints are used in each drink
all_drink_dicts = [
    milk_tea_drink_to_ing,
    fruit_tea_drink_to_ing,
    matcha_tea_drink_to_ing,
    non_caffenited_drink_to_ing,
    ice_blended_drink_to_ing
]

drink_map = {name.strip(): pid for pid, name, price, category in products}

for drink_dict in all_drink_dicts:
    for drink_name, ingridient_list in drink_dict.items():
        product_id = drink_map.get(drink_name.strip())
        for ing in ingridient_list:
            ingredient_id= ingredient_map.get(ing)
            cursor.execute(
            """
            INSERT INTO drink_ingredient (product_id, ingredient_id, quantity_needed)
            VALUES (%s, %s, %s)
            ON CONFLICT (product_id, ingredient_id) DO NOTHING
            """,
            (product_id, ingredient_id, 1)
            )
            

# Commit and close
conn.commit()
cursor.close()
conn.close()

