# How to Run the Python and SQLite Inventory Management System

## 1. Install Python
Download and install Python from https://www.python.org/downloads/. During installation, select **Add Python to PATH**.

To check the installation, open Command Prompt and run:

```bash
python --version
```

## 2. Open the Project
1. Open Visual Studio Code.
2. Open the folder containing the project.
3. Save the source code as `inventory.py`.
4. Open the terminal by selecting **Terminal → New Terminal**.

## 3. Run the Project
Enter the following command in the terminal:

```bash
python inventory.py
```

Replace `inventory.py` with your actual Python filename if it is different.

The main menu will appear:

```text
INVENTORY MANAGEMENT SYSTEM

1. Sign Up
2. Sign In
3. Exit

Enter your choice:
```

## 4. Sign In
The project includes a default owner account.

- **Username:** gopikaa
- **Password:** 12345

Select option 2 to sign in. After successful login, the Owner Dashboard will appear.

You can also select Sign Up to create a new user or owner account.

## 5. Use the System
The Owner Dashboard allows you to manage users, categories and products, record stock-in and stock-out transactions, search products, check low-stock alerts, view transaction history and access inventory summaries.

The User Dashboard allows you to view products, search products, check stock availability and view product details.

Enter the corresponding menu number to access each feature. Select Logout to return to the main menu and Exit to close the application.

## 6. Database
The project uses SQLite, which is included with Python, so no separate database installation is required.

When the program runs, it creates or opens `inventory_system.db`. The database contains four tables:

- **users:** Stores usernames, passwords and roles.
- **categories:** Stores product categories and descriptions.
- **products:** Stores product names, prices, quantities and supplier details.
- **stock_transactions:** Records stock additions and removals with user and date information.

The database preserves saved information between program runs, provided you continue using the same database file.
