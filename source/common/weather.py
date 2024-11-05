import requests

def get_weather(city):
    api_key = ''
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    return response.json()

weather_data = get_weather('Paris')
print(weather_data)  # Will print current weather info for Paris
