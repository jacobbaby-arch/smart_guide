from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

API_KEY = '1feaacfb3e24478cb6837a080b4df36c'

def get_continents():
    # Example of using Geoapify Places API to get continents
    url = f'https://api.geoapify.com/v2/places?categories=continent&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    continents = [{'id': place['place_id'], 'name': place['name'], 'image_path': place['icon']} for place in data['features']]
    return continents

def get_countries_by_continent(continent_id):
    # Example of using Geoapify Places API to get countries by continent
    url = f'https://api.geoapify.com/v2/places?categories=country&filter=continent:{continent_id}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    countries = [{'id': place['place_id'], 'name': place['name'], 'image_path': place['icon']} for place in data['features']]
    return countries

def get_destinations_by_country(country_id):
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'trip_planner.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT destinations.name, destinations.image_path
        FROM destinations
        WHERE destinations.country_id = ?
    ''', (country_id,))
    destinations = cursor.fetchall()
    conn.close()
    return destinations

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'destination_name' in request.form and 'country_id' in request.form and 'destination_image_path' in request.form:
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
        elif 'continent_name' in request.form and 'continent_image_path' in request.form:
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
        return redirect(url_for('admin'))
    continents = get_continents()
    return render_template('admin.html', continents=continents)

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