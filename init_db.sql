-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
-- Create expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date DATE,
    description TEXT
);
-- Create a view with renumbered IDs
CREATE VIEW IF NOT EXISTS expenses_view AS
SELECT ROW_NUMBER() OVER (
        ORDER BY id
    ) AS row_number,
    amount,
    category,
    date,
    description
FROM expenses;