import argparse
import os
from datetime import datetime
from database import create_database, add_expense, view_expenses, renumbered_ids, delete_all_entries, delete_entry_by_id

# CLI Setup
def setup_cli():
    """
    Set up the command-line interface (CLI) using argparse.

    Parameters:
    None

    Returns:
    argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Add Expense Command
    add_expense_parser = subparsers.add_parser("add", help="Add a new expense. Example: add 50.0 Grocery 23-04-2024 \"Weekly grocery shopping\"")
    add_expense_parser.add_argument("amount", type=float, help="Expense amount")
    add_expense_parser.add_argument("category", type=str, help="Expense category")
    add_expense_parser.add_argument("date", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="Expense date (DD-MM-YYYY)")
    add_expense_parser.add_argument("description", type=str, help="Expense description")

    # View Expenses Command
    subparsers.add_parser("view", help="View all expenses")
    
    # Delete Entry Command
    delete_entry_parser = subparsers.add_parser("delete", help="Delete a specific entry by ID/Row")
    delete_entry_parser.add_argument("entry_id", type=int, help="ID/Row of the entry to delete")

    # Delete All Command
    subparsers.add_parser("delete_all", help="Delete all entries")

    # Help Command
    subparsers.add_parser("help", help="Show help information for available commands")

    return parser


def main():
    """
    Main function for the Expense Tracker program.

    Parameters:
    None

    Returns:
    None
    """
    # Check if the database file exists
    database_exists = os.path.isfile("expenses.db")

    if not database_exists:
        print("Welcome to the Expense Tracker!")
        print("To get started, use the following commands:")
        print("  python expense_tracker.py add <amount> <category> <date> \"<description>\"")
        print("  python expense_tracker.py view")
        print("  python expense_tracker.py delete <entry_id>")
        print("  python expense_tracker.py delete_all")
        print("  python expense_tracker.py help")
        print("Note: Make sure to prefix commands with 'python expense_tracker.py'")
    else:
        print("Welcome back to the Expense Tracker!")
        print("To see available commands, use:")
        print("  python expense_tracker.py help")

    create_database()
    renumbered_ids()

    parser = setup_cli()

    try:
        args = parser.parse_args()
        match args.command:
            case "add":
                add_expense(args.amount, args.category, args.date, args.description)
            case "view":
                view_expenses()
            case "delete_all":
                delete_all_entries()
            case "delete":
                delete_entry_by_id(args.entry_id)
            case "help":
                parser.print_help()
            case _:
                pass
    except argparse.ArgumentError as e:
        print(f"ArgumentError: {e}")

if __name__ == "__main__":
    main()