import requests
import sqlite3
import time
import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv('API_KEY')
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def fetch_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    # print(response)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return {
            'city': city,
            'main': data['weather'][0]['main'],
            'temp': data['main']['temp'] - 273.15,  # Convert Kelvin to Celsius
            'feels_like': data['main']['feels_like'] - 273.15,
            'dt': data['dt']
        }
    return None

def store_weather_data(city, weather_data):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO weather (city, main, temp, feels_like, dt)
                      VALUES (?, ?, ?, ?, ?)''', 
                      (city, weather_data['main'], weather_data['temp'], 
                       weather_data['feels_like'], weather_data['dt']))
    conn.commit()
    conn.close()

def fetch_and_store_weather():
    for city in CITIES:
        weather_data = fetch_weather_data(city)
        if weather_data:
            store_weather_data(city, weather_data)

def get_daily_summary():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT city, 
                             ROUND(AVG(temp), 2), 
                             ROUND(MAX(temp), 2), 
                             ROUND(MIN(temp), 2), 
                             (SELECT main FROM weather GROUP BY main 
                              ORDER BY COUNT(*) DESC LIMIT 1)
                      FROM weather
                      WHERE dt > strftime('%s', 'now', 'start of day')
                      GROUP BY city''')
    summary = cursor.fetchall()
    conn.close()
    return summary

# fetch_weather_data('Delhi')