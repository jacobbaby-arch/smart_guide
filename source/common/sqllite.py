import sqlite3

# Connect to the SQLite database (it will create the file if it does not exist)
conn = sqlite3.connect('travel_assistant.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# 3. Create a table
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itineraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT,
            days INTEGER,
            interests TEXT,
            itinerary TEXT
        )
    ''')
    print("Table created successfully.")

# 4. Insert data into the table
def insert_itinerary(destination, days, interests, itinerary):
    cursor.execute('''
        INSERT INTO itineraries (destination, days, interests, itinerary)
        VALUES (?, ?, ?, ?)
    ''', (destination, days, interests, itinerary))
    conn.commit()
    print("Itinerary inserted successfully.")

# 5. Query data from the table
def get_itineraries():
    cursor.execute('SELECT * FROM itineraries')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# 6. Update data in the table
def update_itinerary(id, new_itinerary):
    cursor.execute('''
        UPDATE itineraries
        SET itinerary = ?
        WHERE id = ?
    ''', (new_itinerary, id))
    conn.commit()
    print("Itinerary updated successfully.")

# 7. Delete data from the table
def delete_itinerary(id):
    cursor.execute('''
        DELETE FROM itineraries WHERE id = ?
    ''', (id,))
    conn.commit()
    print("Itinerary deleted successfully.")

# 8. Close the connection
def close_connection():
    cursor.close()
    conn.close()
    print("Connection closed.")

# Example usage
create_table()  # Create table
insert_itinerary("Paris", 5, "history and art", "Day 1: Visit the Louvre, Day 2: Eiffel Tower and museums, ...")
get_itineraries()  # Query all itineraries
update_itinerary(1, "Updated itinerary for Paris with new details.")
get_itineraries()  # Query all itineraries after update
delete_itinerary(1)  # Delete itinerary with id 1
get_itineraries()  # Query again after deletion

close_connection()  # Close the connection
