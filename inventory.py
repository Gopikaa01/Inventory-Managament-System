import sqlite3
from datetime import datetime


con = sqlite3.connect("inventory_system.db")

# Enable foreign key support
con.execute("PRAGMA foreign_keys = ON")


#TABLE1: USERS

con.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")


#TABLE 2: CATEGORIES

con.execute("""
CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL,
    description TEXT
)
""")


#TABLE 3: PRODUCTS

con.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT UNIQUE NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    supplier TEXT,
    FOREIGN KEY(category_id)
    REFERENCES categories(category_id)
)
""")


# TABLE 4: STOCK TRANSACTIONS

con.execute("""
CREATE TABLE IF NOT EXISTS stock_transactions(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    transaction_date TEXT NOT NULL,
    FOREIGN KEY(product_id)
    REFERENCES products(product_id),
    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
)
""")


con.commit()


# DEFAULT OWNER ACCOUNT
con.execute("""
INSERT OR IGNORE INTO users(username,password,role)
VALUES('gopikaa','12345','owner')
""")

con.commit()


# SAMPLE CATEGORIES
con.execute("""
INSERT OR IGNORE INTO categories(category_name,description)
VALUES('Electronics','Electronic products')
""")

con.execute("""
INSERT OR IGNORE INTO categories(category_name,description)
VALUES('Accessories','Computer and electronic accessories')
""")

con.execute("""
INSERT OR IGNORE INTO categories(category_name,description)
VALUES('Computer','Computer related products')
""")

con.commit()


# SAMPLE PRODUCTS
con.execute("""
INSERT OR IGNORE INTO products
(product_name,category_id,price,quantity,supplier)
VALUES('Raspberry Pi',1,5000,10,'Raspberry Pi Supplier')
""")

con.execute("""
INSERT OR IGNORE INTO products
(product_name,category_id,price,quantity,supplier)
VALUES('Arduino Uno',1,800,15,'Arduino Supplier')
""")

con.execute("""
INSERT OR IGNORE INTO products
(product_name,category_id,price,quantity,supplier)
VALUES('USB Cable',2,150,25,'ABC Electronics')
""")

con.execute("""
INSERT OR IGNORE INTO products
(product_name,category_id,price,quantity,supplier)
VALUES('Keyboard',3,700,12,'Computer World')
""")

con.execute("""
INSERT OR IGNORE INTO products
(product_name,category_id,price,quantity,supplier)
VALUES('Mouse',3,400,20,'Computer World')
""")

con.commit()


# SIGN UP


def signup():

    print("\n---------- SIGN UP ----------")

    print("1. User")
    print("2. Owner")

    role_choice = input("Choose role: ")

    if role_choice == "1":
        role = "user"

    elif role_choice == "2":
        role = "owner"

    else:
        print("Invalid choice.")
        return

    username = input("Enter username: ")
    password = input("Enter password: ")

    if len(password) < 4:
        print("Password should contain atleast 4 characters.")
        return

    try:

        con.execute("""
        INSERT INTO users(username,password,role)
        VALUES(?,?,?)
        """,(username,password,role))

        con.commit()

        print("Registration successful.")

    except sqlite3.IntegrityError:

        print("Username already exists.")


# SIGN IN


def signin():

    print("\n---------- SIGN IN ----------")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if len(password) < 4:
        print("Password should contain atleast 4 characters.")
        return

    result = con.execute("""
    SELECT user_id,username,role
    FROM users
    WHERE username=? AND password=?
    """,(username,password))

    user = result.fetchone()

    if user:

        print("\nLogin successful.")
        print("Welcome,",user[1])
        print("Role:",user[2])

        if user[2] == "owner":

            owner_dashboard(user[0])

        elif user[2] == "user":

            user_dashboard(user[0])

    else:

        print("Invalid username or password.")



# USER DASHBOARD


def user_dashboard(user_id):

    while True:

        print("\n---------- USER DASHBOARD ----------")

        print("1. View Products")
        print("2. Search Products")
        print("3. Check Stock Availability")
        print("4. View Product Details")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":

            view_products()

        elif choice == "2":

            search_products()

        elif choice == "3":

            check_stock()

        elif choice == "4":

            view_product_details()

        elif choice == "5":

            print("Logged out successfully.")
            break

        else:

            print("Invalid choice.")



# OWNER DASHBOARD


def owner_dashboard(user_id):

    while True:

        print("\n---------- OWNER DASHBOARD ----------")

        print("1. User Management")
        print("2. Category Management")
        print("3. Product Management")
        print("4. Stock In")
        print("5. Stock Out")
        print("6. View Stock Transactions")
        print("7. Search Products")
        print("8. Check Low Stock")
        print("9. Inventory Overview")
        print("10. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":

            user_management()

        elif choice == "2":

            category_management()

        elif choice == "3":

            product_management()

        elif choice == "4":

            stock_in(user_id)

        elif choice == "5":

            stock_out(user_id)

        elif choice == "6":

            view_transactions()

        elif choice == "7":

            search_products()

        elif choice == "8":

            low_stock_alert()

        elif choice == "9":

            inventory_overview()

        elif choice == "10":

            print("Logged out successfully.")
            break

        else:

            print("Invalid choice.")


# USER MANAGEMENT


def user_management():

    while True:

        print("\n---------- USER MANAGEMENT ----------")

        print("1. Add User")
        print("2. View Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Back")

        choice = input("Enter your choice: ")

        if choice == "1":

            add_user()

        elif choice == "2":

            view_users()

        elif choice == "3":

            update_user()

        elif choice == "4":

            delete_user()

        elif choice == "5":

            break

        else:

            print("Invalid choice.")



# ADD USER


def add_user():

    print("\n---------- ADD USER ----------")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if len(password) < 4:

        print("Password should contain atleast 4 characters.")
        return

    print("1. User")
    print("2. Owner")

    choice = input("Choose role: ")

    if choice == "1":

        role = "user"

    elif choice == "2":

        role = "owner"

    else:

        print("Invalid choice.")
        return

    try:

        con.execute("""
        INSERT INTO users(username,password,role)
        VALUES(?,?,?)
        """,(username,password,role))

        con.commit()

        print("User added successfully.")

    except sqlite3.IntegrityError:

        print("Username already exists.")


# ============================================================
# VIEW USERS
# ============================================================

def view_users():

    print("\n---------- USERS ----------")

    result = con.execute("""
    SELECT user_id,username,role
    FROM users
    """)

    users = result.fetchall()

    if not users:

        print("No users available.")

    else:

        for user in users:

            print("\nUser ID :",user[0])
            print("Username:",user[1])
            print("Role    :",user[2])


# ============================================================
# UPDATE USER
# ============================================================

def update_user():

    print("\n---------- UPDATE USER ----------")

    user_id = input("Enter user ID: ")

    result = con.execute("""
    SELECT user_id
    FROM users
    WHERE user_id=?
    """,(user_id,))

    user = result.fetchone()

    if not user:

        print("User not found.")
        return

    username = input("Enter new username: ")
    password = input("Enter new password: ")

    if len(password) < 4:

        print("Password should contain atleast 4 characters.")
        return

    print("1. User")
    print("2. Owner")

    choice = input("Choose role: ")

    if choice == "1":

        role = "user"

    elif choice == "2":

        role = "owner"

    else:

        print("Invalid choice.")
        return

    try:

        con.execute("""
        UPDATE users
        SET username=?,password=?,role=?
        WHERE user_id=?
        """,(username,password,role,user_id))

        con.commit()

        print("User updated successfully.")

    except sqlite3.IntegrityError:

        print("Username already exists.")



# DELETE USER
def delete_user():

    print("\n---------- DELETE USER ----------")

    user_id = input("Enter user ID: ")

    try:

        con.execute("""
        DELETE FROM users
        WHERE user_id=?
        """,(user_id,))

        con.commit()

        print("User deleted successfully.")

    except sqlite3.IntegrityError:

        print("Cannot delete user because stock transactions exist.")



# CATEGORY MANAGEMENT
def category_management():

    while True:

        print("\n---------- CATEGORY MANAGEMENT ----------")

        print("1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("5. Back")

        choice = input("Enter your choice: ")

        if choice == "1":

            add_category()

        elif choice == "2":

            view_categories()

        elif choice == "3":

            update_category()

        elif choice == "4":

            delete_category()

        elif choice == "5":

            break

        else:

            print("Invalid choice.")



# ADD CATEGORY
def add_category():

    print("\n---------- ADD CATEGORY ----------")

    name = input("Enter category name: ")
    description = input("Enter category description: ")

    try:

        con.execute("""
        INSERT INTO categories(category_name,description)
        VALUES(?,?)
        """,(name,description))

        con.commit()

        print("Category added successfully.")

    except sqlite3.IntegrityError:

        print("Category already exists.")



# VIEW CATEGORIES
def view_categories():

    print("\n---------- CATEGORIES ----------")

    result = con.execute("""
    SELECT category_id,category_name,description
    FROM categories
    """)

    categories = result.fetchall()

    if not categories:

        print("No categories available.")

    else:

        for category in categories:

            print("\nCategory ID :",category[0])
            print("Category    :",category[1])
            print("Description :",category[2])


# UPDATE CATEGORY
def update_category():

    print("\n---------- UPDATE CATEGORY ----------")

    category_id = input("Enter category ID: ")

    result = con.execute("""
    SELECT category_id
    FROM categories
    WHERE category_id=?
    """,(category_id,))

    category = result.fetchone()

    if not category:

        print("Category not found.")
        return

    name = input("Enter new category name: ")
    description = input("Enter new description: ")

    try:

        con.execute("""
        UPDATE categories
        SET category_name=?,description=?
        WHERE category_id=?
        """,(name,description,category_id))

        con.commit()

        print("Category updated successfully.")

    except sqlite3.IntegrityError:

        print("Category name already exists.")



# DELETE CATEGORY
def delete_category():

    print("\n---------- DELETE CATEGORY ----------")

    category_id = input("Enter category ID: ")

    result = con.execute("""
    SELECT product_id
    FROM products
    WHERE category_id=?
    """,(category_id,))

    products = result.fetchall()

    if products:

        print("Cannot delete category because products are using it.")
        return

    con.execute("""
    DELETE FROM categories
    WHERE category_id=?
    """,(category_id,))

    con.commit()

    print("Category deleted successfully.")


# PRODUCT MANAGEMENT
def product_management():

    while True:

        print("\n---------- PRODUCT MANAGEMENT ----------")

        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Back")

        choice = input("Enter your choice: ")

        if choice == "1":

            add_product()

        elif choice == "2":

            view_products()

        elif choice == "3":

            update_product()

        elif choice == "4":

            delete_product()

        elif choice == "5":

            break

        else:

            print("Invalid choice.")



# ADD PRODUCT
def add_product():

    print("\n---------- ADD PRODUCT ----------")

    product_name = input("Enter product name: ")

    view_categories()

    category_id = input("\nEnter category ID: ")

    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))

    supplier = input("Enter supplier name: ")

    if price < 0 or quantity < 0:

        print("Price and quantity cannot be negative.")
        return

    try:

        con.execute("""
        INSERT INTO products
        (product_name,category_id,price,quantity,supplier)
        VALUES(?,?,?,?,?)
        """,
        (product_name,category_id,price,quantity,supplier))

        con.commit()

        print("Product added successfully.")

    except sqlite3.IntegrityError:

        print("Product already exists or category is invalid.")



# VIEW PRODUCTS
def view_products():

    print("\n---------- PRODUCTS ----------")

    result = con.execute("""
    SELECT
        products.product_id,
        products.product_name,
        categories.category_name,
        products.price,
        products.quantity,
        products.supplier
    FROM products
    JOIN categories
    ON products.category_id=categories.category_id
    """)

    products = result.fetchall()

    if not products:

        print("No products available.")

    else:

        for product in products:

            print("\nProduct ID :",product[0])
            print("Product    :",product[1])
            print("Category   :",product[2])
            print("Price      :",product[3])
            print("Quantity   :",product[4])
            print("Supplier   :",product[5])


# UPDATE PRODUCT
def update_product():

    print("\n---------- UPDATE PRODUCT ----------")

    product_id = input("Enter product ID: ")

    result = con.execute("""
    SELECT product_id
    FROM products
    WHERE product_id=?
    """,(product_id,))

    product = result.fetchone()

    if not product:

        print("Product not found.")
        return

    product_name = input("Enter new product name: ")

    view_categories()

    category_id = input("\nEnter new category ID: ")

    price = float(input("Enter new price: "))
    quantity = int(input("Enter new quantity: "))
    supplier = input("Enter new supplier: ")

    if price < 0 or quantity < 0:

        print("Price and quantity cannot be negative.")
        return

    try:

        con.execute("""
        UPDATE products
        SET product_name=?,
            category_id=?,
            price=?,
            quantity=?,
            supplier=?
        WHERE product_id=?
        """,
        (product_name,category_id,price,quantity,supplier,product_id))

        con.commit()

        print("Product updated successfully.")

    except sqlite3.IntegrityError:

        print("Product name already exists or category is invalid.")


# ============================================================
# DELETE PRODUCT
# ============================================================

def delete_product():

    print("\n---------- DELETE PRODUCT ----------")

    product_id = input("Enter product ID: ")

    result = con.execute("""
    SELECT transaction_id
    FROM stock_transactions
    WHERE product_id=?
    """,(product_id,))

    transactions = result.fetchall()

    if transactions:

        print("Cannot delete product because stock transactions exist.")
        return

    con.execute("""
    DELETE FROM products
    WHERE product_id=?
    """,(product_id,))

    con.commit()

    print("Product deleted successfully.")


# STOCK IN
def stock_in(user_id):

    print("\n---------- STOCK IN ----------")

    product_id = input("Enter product ID: ")
    quantity = int(input("Enter quantity: "))

    if quantity <= 0:

        print("Quantity should be greater than zero.")
        return

    result = con.execute("""
    SELECT product_id,product_name
    FROM products
    WHERE product_id=?
    """,(product_id,))

    product = result.fetchone()

    if not product:

        print("Product not found.")
        return

    con.execute("""
    UPDATE products
    SET quantity=quantity+?
    WHERE product_id=?
    """,(quantity,product_id))

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    con.execute("""
    INSERT INTO stock_transactions
    (product_id,user_id,transaction_type,quantity,transaction_date)
    VALUES(?,?,?,?,?)
    """,
    (product_id,user_id,"IN",quantity,date))

    con.commit()

    print("Stock added successfully.")


# STOCK OUT
def stock_out(user_id):

    print("\n---------- STOCK OUT ----------")

    product_id = input("Enter product ID: ")
    quantity = int(input("Enter quantity: "))

    if quantity <= 0:

        print("Quantity should be greater than zero.")
        return

    result = con.execute("""
    SELECT product_id,product_name,quantity
    FROM products
    WHERE product_id=?
    """,(product_id,))

    product = result.fetchone()

    if not product:

        print("Product not found.")
        return

    if quantity > product[2]:

        print("Not enough stock available.")
        return

    con.execute("""
    UPDATE products
    SET quantity=quantity-?
    WHERE product_id=?
    """,(quantity,product_id))

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    con.execute("""
    INSERT INTO stock_transactions
    (product_id,user_id,transaction_type,quantity,transaction_date)
    VALUES(?,?,?,?,?)
    """,
    (product_id,user_id,"OUT",quantity,date))

    con.commit()

    print("Stock removed successfully.")



# VIEW STOCK TRANSACTIONS
def view_transactions():

    print("\n---------- STOCK TRANSACTIONS ----------")

    result = con.execute("""
    SELECT
        stock_transactions.transaction_id,
        products.product_name,
        users.username,
        stock_transactions.transaction_type,
        stock_transactions.quantity,
        stock_transactions.transaction_date
    FROM stock_transactions
    JOIN products
    ON stock_transactions.product_id=products.product_id
    JOIN users
    ON stock_transactions.user_id=users.user_id
    """)

    transactions = result.fetchall()

    if not transactions:

        print("No stock transactions available.")

    else:

        for transaction in transactions:

            print("\nTransaction ID :",transaction[0])
            print("Product        :",transaction[1])
            print("User           :",transaction[2])
            print("Type           :",transaction[3])
            print("Quantity       :",transaction[4])
            print("Date           :",transaction[5])



# SEARCH PRODUCTS
def search_products():

    print("\n---------- SEARCH PRODUCTS ----------")

    name = input("Enter product name: ")

    result = con.execute("""
    SELECT
        products.product_id,
        products.product_name,
        categories.category_name,
        products.price,
        products.quantity,
        products.supplier
    FROM products
    JOIN categories
    ON products.category_id=categories.category_id
    WHERE products.product_name LIKE ?
    """,("%"+name+"%",))

    products = result.fetchall()

    if not products:

        print("No matching products found.")

    else:

        for product in products:

            print("\nProduct ID :",product[0])
            print("Product    :",product[1])
            print("Category   :",product[2])
            print("Price      :",product[3])
            print("Quantity   :",product[4])
            print("Supplier   :",product[5])



# CHECK STOCK
def check_stock():

    print("\n---------- CHECK STOCK ----------")

    product_id = input("Enter product ID: ")

    result = con.execute("""
    SELECT product_name,quantity
    FROM products
    WHERE product_id=?
    """,(product_id,))

    product = result.fetchone()

    if product:

        print("Product :",product[0])
        print("Stock   :",product[1])

        if product[1] == 0:

            print("Status  : Out of stock")

        elif product[1] <= 5:

            print("Status  : Low stock")

        else:

            print("Status  : Available")

    else:

        print("Product not found.")



# VIEW PRODUCT DETAILS
def view_product_details():

    print("\n---------- PRODUCT DETAILS ----------")

    product_id = input("Enter product ID: ")

    result = con.execute("""
    SELECT
        products.product_id,
        products.product_name,
        categories.category_name,
        categories.description,
        products.price,
        products.quantity,
        products.supplier
    FROM products
    JOIN categories
    ON products.category_id=categories.category_id
    WHERE products.product_id=?
    """,(product_id,))

    product = result.fetchone()

    if product:

        print("\nProduct ID   :",product[0])
        print("Product      :",product[1])
        print("Category     :",product[2])
        print("Description  :",product[3])
        print("Price        :",product[4])
        print("Quantity     :",product[5])
        print("Supplier     :",product[6])

    else:

        print("Product not found.")


# LOW STOCK ALERT
def low_stock_alert():

    print("\n---------- LOW STOCK ALERT ----------")

    result = con.execute("""
    SELECT
        product_id,
        product_name,
        quantity
    FROM products
    WHERE quantity <= 5
    """)

    products = result.fetchall()

    if not products:

        print("No low stock products.")

    else:

        for product in products:

            print("\nProduct ID :",product[0])
            print("Product    :",product[1])
            print("Quantity   :",product[2])



# INVENTORY OVERVIEW
def inventory_overview():

    print("\n---------- INVENTORY OVERVIEW ----------")

    result = con.execute("""
    SELECT COUNT(*),SUM(quantity)
    FROM products
    """)

    data = result.fetchone()

    total_products = data[0]
    total_quantity = data[1]

    if total_quantity is None:

        total_quantity = 0

    print("Total Products :",total_products)
    print("Total Stock    :",total_quantity)

    result = con.execute("""
    SELECT COUNT(*)
    FROM products
    WHERE quantity <= 5
    """)

    low_stock = result.fetchone()[0]

    print("Low Stock Items:",low_stock)


# MAIN MENU
while True:

    print("\n")
    print("================================================================")
    print("                 INVENTORY MANAGEMENT SYSTEM")
    print("================================================================")

    print("\n1. Sign Up")
    print("2. Sign In")
    print("3. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        signup()

    elif choice == "2":

        signin()

    elif choice == "3":

        print("Thank you for using Inventory Management System.")
        break

    else:

        print("Invalid choice.")



con.close()