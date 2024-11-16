import sqlite3
import os

# Ensure the db directory exists
os.makedirs('./src/db', exist_ok=True)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('./src/db/trip_planner.db')

# Create a cursor object
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS continents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    image_path TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    continent_id INTEGER,
    image_path TEXT,
    FOREIGN KEY (continent_id) REFERENCES continents (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country_id INTEGER,
    image_path TEXT,
    FOREIGN KEY (country_id) REFERENCES countries (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attractions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    destination_id INTEGER,
    FOREIGN KEY (destination_id) REFERENCES destinations (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS itineraries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day INTEGER NOT NULL,
    description TEXT NOT NULL,
    destination_id INTEGER,
    FOREIGN KEY (destination_id) REFERENCES destinations (id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()