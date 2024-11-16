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

# Insert initial data into attractions table
attractions = [
    ('Tokyo Tower', 'A communications and observation tower in the Shiba-koen district of Minato, Tokyo, Japan.', 'images/tokyo_tower.jpg', 1),
    ('Great Wall of China', 'A series of fortifications made of stone, brick, tamped earth, wood, and other materials.', 'images/great_wall_of_china.jpg', 2),
    ('Grand Palace', 'A complex of buildings at the heart of Bangkok, Thailand.', 'images/grand_palace.jpg', 3),
    ('Eiffel Tower', 'A wrought-iron lattice tower on the Champ de Mars in Paris, France.', 'images/eiffel_tower.jpg', 4),
    ('Brandenburg Gate', 'An 18th-century neoclassical monument in Berlin, Germany.', 'images/brandenburg_gate.jpg', 5),
    ('Colosseum', 'An ancient amphitheater in Rome, Italy.', 'images/colosseum.jpg', 6),
    ('Statue of Liberty', 'A colossal neoclassical sculpture on Liberty Island in New York Harbor.', 'images/statue_of_liberty.jpg', 7),
    ('CN Tower', 'A 553.3 m-high concrete communications and observation tower in downtown Toronto, Ontario, Canada.', 'images/cn_tower.jpg', 8),
    ('Christ the Redeemer', 'An Art Deco statue of Jesus Christ in Rio de Janeiro, Brazil.', 'images/christ_the_redeemer.jpg', 9)
]

cursor.executemany('''
INSERT INTO attractions (name, description, image_path, destination_id)
VALUES (?, ?, ?, ?)
''', attractions)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")