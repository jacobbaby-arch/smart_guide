from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

ADMIN_PASSCODE = '1234'  # Replace with your actual passcode

def get_continents():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, image_path FROM continents')
    continents = cursor.fetchall()
    conn.close()
    return continents

def get_countries():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM countries')
    countries = cursor.fetchall()
    conn.close()
    return countries

def get_destinations():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM destinations')
    destinations = cursor.fetchall()
    conn.close()
    return destinations

def get_countries_by_continent(continent_id):
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT countries.id, countries.name, countries.image_path
        FROM countries
        WHERE countries.continent_id = ?
    ''', (continent_id,))
    countries = cursor.fetchall()
    conn.close()
    return countries

def get_destinations_by_country(country_id):
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT destinations.id, destinations.name, destinations.image_path
        FROM destinations
        WHERE destinations.country_id = ?
    ''', (country_id,))
    destinations = cursor.fetchall()
    conn.close()
    return destinations

def get_all_countries_and_destinations():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT countries.id, countries.name, destinations.id, destinations.name
        FROM countries
        JOIN destinations ON countries.id = destinations.country_id
    ''')
    data = cursor.fetchall()
    countries = {}
    for country_id, country_name, destination_id, destination_name in data:
        if country_id not in countries:
            countries[country_id] = [country_name, []]
        countries[country_id][1].append((destination_id, destination_name))
    conn.close()
    return countries
    
def get_attractions_by_destination(destination_id):
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, description, image_path
        FROM attractions
        WHERE destination_id = ?
    ''', (destination_id,))
    attractions = cursor.fetchall()
    conn.close()
    return attractions

def get_itineraries_by_destination(destination_id):
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT day, description
        FROM itineraries
        WHERE destination_id = ?
    ''', (destination_id,))
    itineraries = cursor.fetchall()
    conn.close()
    return itineraries

@app.route('/')
def index():
    continents = get_continents()
    return render_template('index.html', continents=continents)

@app.route('/countries/<int:continent_id>')
def countries(continent_id):
    countries = get_countries_by_continent(continent_id)
    return render_template('countries.html', countries=countries)

@app.route('/destinations/<int:country_id>')
def destinations(country_id):
    destinations = get_destinations_by_country(country_id)
    return render_template('destinations.html', destinations=destinations)

@app.route('/attractions/<int:destination_id>')
def attractions(destination_id):
    attractions = get_attractions_by_destination(destination_id)
    return jsonify({'attractions': [{'name': attraction[0], 'description': attraction[1], 'image_path': attraction[2]} for attraction in attractions]})

@app.route('/itineraries/<int:destination_id>')
def itineraries(destination_id):
    itineraries = get_itineraries_by_destination(destination_id)
    return jsonify({'itineraries': [{'day': itinerary[0], 'description': itinerary[1]} for itinerary in itineraries]})

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'passcode' in request.form:
            passcode = request.form['passcode']
            if passcode == ADMIN_PASSCODE:
                session['admin_authenticated'] = True
                return redirect(url_for('admin'))
            else:
                flash('Incorrect passcode. Please try again.')
                return redirect(url_for('admin'))
        if not session.get('admin_authenticated'):
            flash('You must enter the passcode to access the admin page.')
            return redirect(url_for('admin'))
        if 'continent_name' in request.form and 'continent_image_path' in request.form:
            continent_name = request.form['continent_name']
            continent_image_path = request.form['continent_image_path']
            db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO continents (name, image_path)
                VALUES (?, ?)
            ''', (continent_name, continent_image_path))
            conn.commit()
            conn.close()
            flash('Continent added successfully!')
        elif 'country_name' in request.form and 'continent_id' in request.form and 'country_image_path' in request.form:
            country_name = request.form['country_name']
            continent_id = request.form['continent_id']
            country_image_path = request.form['country_image_path']
            db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO countries (name, continent_id, image_path)
                VALUES (?, ?, ?)
            ''', (country_name, continent_id, country_image_path))
            conn.commit()
            conn.close()
            flash('Country added successfully!')
        elif 'destination_name' in request.form and 'country_id' in request.form and 'destination_image_path' in request.form:
            destination_name = request.form['destination_name']
            country_id = request.form['country_id']
            destination_image_path = request.form['destination_image_path']
            db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO destinations (name, country_id, image_path)
                VALUES (?, ?, ?)
            ''', (destination_name, country_id, destination_image_path))
            conn.commit()
            conn.close()
            flash('Destination added successfully!')
        elif 'attraction_name' in request.form and 'attraction_description' in request.form and 'destination_id' in request.form and 'attraction_image_path' in request.form:
            attraction_name = request.form['attraction_name']
            attraction_description = request.form['attraction_description']
            destination_id = request.form['destination_id']
            attraction_image_path = request.form['attraction_image_path']
            db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO attractions (name, description, image_path, destination_id)
                VALUES (?, ?, ?, ?)
            ''', (attraction_name, attraction_description, attraction_image_path, destination_id))
            conn.commit()
            conn.close()
            flash('Attraction added successfully!')
        elif 'itinerary_day' in request.form and 'itinerary_description' in request.form and 'destination_id' in request.form:
            itinerary_day = request.form['itinerary_day']
            itinerary_description = request.form['itinerary_description']
            destination_id = request.form['destination_id']
            db_path = os.path.join(os.path.dirname(__file__), 'src/db', 'trip_planner.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO itineraries (day, description, destination_id)
                VALUES (?, ?, ?)
            ''', (itinerary_day, itinerary_description, destination_id))
            conn.commit()
            conn.close()
            flash('Itinerary added successfully!')
        return redirect(url_for('admin'))
    if not session.get('admin_authenticated'):
        return render_template('admin_login.html')
    continents = get_continents()
    countries = get_countries()
    destinations = get_destinations()
    all_countries_and_destinations = get_all_countries_and_destinations()
    #session.pop('admin_authenticated', None)  # Clear the session variable after each request
    return render_template('admin.html', continents=continents, countries=countries, destinations=destinations, all_countries_and_destinations=all_countries_and_destinations)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission here (e.g., save to database, send email, etc.)
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # For now, just print the form data to the console
        print(f"Name: {name}, Email: {email}, Message: {message}")
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)