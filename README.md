# Expense-Tracker-CLI

A simple CLI application for tracking expenses. Users can input, categorize, and manage their expenses through simple text-based commands.

## Quick Start

### For Non-Python Users

If you're not familiar with Python or just want to try out the Expense Tracker quickly, follow these steps:

1. **Download the Executable:**
   - Go to the [Releases](https://github.com/Kevin-CS/Expense-Tracker-CLI/releases) page on GitHub.
   - Download the latest release that includes the `cli.exe` executable.

2. **Run the Executable:**
   - Once downloaded, you can run the `cli.exe` directly on your Windows machine.
   - The executable is a standalone version of the Expense Tracker that doesn't require Python installation.

3. **Follow On-Screen Instructions:**
   - The Expense Tracker CLI will prompt you with instructions on how to add expenses, view them, and perform other actions.

### For Python Users (Advanced Usage)

If you're comfortable with Python or want to explore the source code, refer to the [Source Code](#project-structure) section for instructions on setting up and running the CLI using Python.

## Running the CLI

If you have Python installed, you can also run the CLI directly using the `cli.py` script. Open a terminal and navigate to the project directory, then run: `python cli.py`

## Project Structure

The project is organized as follows:

- **Source Code:**
  - `database.py`: Contains functions for database operations.
  - `cli.py`: Handles the command-line interface and main execution.
  - `README.md`: Provides documentation and instructions for users.

- **Database Initialization Script:**
  - `init_db.sql`: An SQL script for initializing the database schema. Users can use this script to set up the database.

- **Executable (Optional):**
  - Include the `dist/` directory if you choose to create an executable using PyInstaller.

- **Dependencies and Environment:**
  - `requirements.txt`: Lists the Python dependencies required for the project. Users can install these dependencies using `pip install -r requirements.txt`.

## Database Initialization

To initialize the database, run the `init_db.sql` script. You can use a SQLite command-line tool or execute the script using your preferred SQL client.
