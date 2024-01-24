import argparse
import os
from datetime import datetime
import shlex
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


def run_expense_tracker(first_run):
    #print("Inside run_expense_tracker function.")
    
    if first_run:
        print("First run.")
        print("Welcome to the Expense Tracker!")
        print("To get started, use the following commands:")
        print("  add <amount> <category> <date> \"<description>\"")
        print("  view")
        print("  delete <entry_id>")
        print("  delete_all")
        print("  help")
        print("Note: No need to prefix commands with 'python' or use file extension.")
    
    else:
        print("Welcome back to the Expense Tracker!")
        print("To see available commands, use:")
        print("  help")

    parser = setup_cli()
    
    while True:
        try:
            # If no command-line arguments, use interactive input
            user_input = input("Enter command: ")
            args = parser.parse_args(shlex.split(user_input))
        
            #print(f"Parsed arguments: {args}")
        
            match args.command:
                case "add":
                    #print("Executing 'add' command.")
                    add_expense(args.amount, args.category, args.date, args.description)
                case "view":
                    print("Executing 'view' command.")
                    view_expenses()
                case "delete_all":
                    #print("Executing 'delete_all' command.")
                    delete_all_entries()
                case "delete":
                    print("Executing 'delete' command.")
                    delete_entry_by_id(args.entry_id)
                case "help":
                    #print("Executing 'help' command.")
                    parser.print_help()
                case _:
                    print("No valid command.")

        except argparse.ArgumentError as e:
            print(f"ArgumentError: {e}")
            
                               

if __name__ == "__main__":
    first_run = not os.path.isfile("expenses.db")

    create_database()
    

    print("Please enter a letter to coninue or type 'exit' to quit: ")
    user_input = input().lower()

    while user_input != 'exit':
        if user_input.strip():
            try:
                run_expense_tracker(first_run)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        print("Please enter a letter to coninue or type 'exit' to quit: ")
        user_input = input().lower()
        first_run = False  # Set to False after the first run