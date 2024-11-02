import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
connection = sqlite3.connect('book_catalogue.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
''')

# Create Books table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    page_count INTEGER,
    average_rating REAL,
    thumbnail TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
''')

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database and tables created successfully.")
