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

# Insert initial data into continents table
continents = [
    ('Asia', 'images/asia.jpg'),
    ('Europe', 'images/europe.jpg'),
    ('America', 'images/america.jpg')
]

cursor.executemany('''
INSERT INTO continents (name, image_path)
VALUES (?, ?)
''', continents)

# Insert initial data into countries table
countries = [
    ('Japan', 1, 'images/japan.jpg'),
    ('China', 1, 'images/china.jpg'),
    ('Thailand', 1, 'images/thailand.jpg'),
    ('France', 2, 'images/france.jpg'),
    ('Germany', 2, 'images/germany.jpg'),
    ('Italy', 2, 'images/italy.jpg'),
    ('USA', 3, 'images/usa.jpg'),
    ('Canada', 3, 'images/canada.jpg'),
    ('Brazil', 3, 'images/brazil.jpg')
]

cursor.executemany('''
INSERT INTO countries (name, continent_id, image_path)
VALUES (?, ?, ?)
''', countries)

# Insert initial data into destinations table
destinations = [
    ('Tokyo', 1, 'images/tokyo.jpg'),
    ('Beijing', 2, 'images/beijing.jpg'),
    ('Bangkok', 3, 'images/bangkok.jpg'),
    ('Paris', 4, 'images/paris.jpg'),
    ('Berlin', 5, 'images/berlin.jpg'),
    ('Rome', 6, 'images/rome.jpg'),
    ('New York', 7, 'images/new_york.jpg'),
    ('Toronto', 8, 'images/toronto.jpg'),
    ('Rio de Janeiro', 9, 'images/rio.jpg')
]

cursor.executemany('''
INSERT INTO destinations (name, country_id, image_path)
VALUES (?, ?, ?)
''', destinations)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")