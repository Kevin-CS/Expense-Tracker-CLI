import sqlite3
import os
from datetime import datetime

# Configure DB path
db_filename = "expenses.db"  
db_dir = os.path.join(os.getcwd(), "data")
db_path = os.path.join(db_dir, db_filename)
os.makedirs(db_dir, exist_ok=True)

# Database Creation
def create_database():
    """
    Create the SQLite database and necessary tables (expenses and categories).

    Parameters:
    None

    Returns:
    None
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            create_expenses_table = """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                date DATE,
                description TEXT
            );
            """

            create_categories_table = """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            );
            """

            cursor.execute(create_expenses_table)
            cursor.execute(create_categories_table)
            
            renumbered_ids()

    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")


# add a new expense
def add_expense(amount, category, date, description):
    """
    Add a new expense to the database.

    Parameters:
    - amount (float): The expense amount.
    - category (str): The expense category.
    - date (datetime): The expense date.
    - description (str): The expense description.

    Returns:
    None
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Check if the category exists, if not, add it
            cursor.execute("SELECT id FROM categories WHERE name=?", (category,))
            existing_category = cursor.fetchone()

            if not existing_category:
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))

            # Convert the date parameter to a datetime object if it's not already
            if not isinstance(date, datetime):
                try:
                    date_object = datetime.strptime(date, "%d-%m-%Y")
                except ValueError:
                    date_object = datetime.strptime(date, "%Y-%m-%d")
            else:
                date_object = date

            # Store the date as a datetime object in the database
            insert_query = "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?);"
            cursor.execute(insert_query, (amount, category, date_object, description))

            conn.commit()

            print(f"Expense added\nAmount: {amount}\nCategory: {category}\nDate: {date_object.strftime('%d-%m-%Y')}\nDescription: {description}")

    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")



# view all expenses
def view_expenses():
    """
    View all expenses stored in the database.

    Parameters:
    None

    Returns:
    None
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            select_query = "SELECT * FROM expenses_view;"
            cursor.execute(select_query)
            expenses = cursor.fetchall()

            if not expenses:
                print("No expenses found.")
            else:
                 # Display column headers
                print("{:<5} {:<10} {:<10} {:<20} {:<50}".format("Row", "Amount", "Category", "Date", "Description"))
                print("-" * 100)

                for expense in expenses:
                    try:
                        # Convert the date value to a datetime object
                        date_value = datetime.strptime(expense[3], "%Y-%m-%d %H:%M:%S")

                        # Format the date
                        formatted_date = f"{date_value.strftime('%d-%m-%Y'):<20}"
                        print(f"{expense[0]:<5} {expense[1]:<10} {expense[2]:<10} {formatted_date} {expense[4]:<50}")
                    except ValueError as e:
                        print(f"Error: Unable to format date for expense ID {expense[0]}. {e}")
                        break

    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")



# create a view with renumbered IDs
def renumbered_ids():
    """
    Create a view with renumbered IDs in the database.

    Parameters:
    None

    Returns:
    None
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name='expenses_view';")
            view_exists = cursor.fetchone()

            if view_exists:
                cursor.execute("DROP VIEW IF EXISTS expenses_view;")
            # Create a view with renumbered IDs
            cursor.execute("""
                CREATE VIEW expenses_view AS
                SELECT ROW_NUMBER() OVER (ORDER BY id) AS row_number, amount, category, date, description
                FROM expenses;
            """)
            print("View 'expenses_view' created successfully.")
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")

    finally:
        conn.commit()

def delete_all_entries():
    """
    Delete all entries from the expenses and categories tables.

    Parameters:
    None

    Returns:
    None
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM expenses;")
        cursor.execute("DELETE FROM categories;")
        print("All entries deleted successfully.")
    except Exception as e:
        print(f"Error deleting entries: {e}")
    finally:
        conn.commit()

def delete_entry_by_id(entry_id):
    """
    Delete a specific entry by ID from the expenses table.

    Parameters:
    - entry_id (int): The ID of the entry to delete.

    Returns:
    None
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id=?", (entry_id,))
            print(f"Entry with ID {entry_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting entry with ID {entry_id}: {e}")
        
def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%d-%m-%Y")
    except ValueError:
        return datetime.strptime(date_string, "%Y-%m-%d")