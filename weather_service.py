import requests
import sqlite3
import time
import os
from dotenv import load_dotenv


load_dotenv()


API_KEY = '5faccc0dd8528890032646db6c6b6027'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def display_weather_info(units):
    data = get_daily_summary()
    #for city, avg_temp, max_temp, min_temp, condition in data:
    print(data)

def convert_temperature(temp, from_unit, to_unit):
    if from_unit == to_unit:
        return temp

    if from_unit == 'C':
        if to_unit == 'F':
            return (temp * 9/5) + 32
        elif to_unit == 'K':
            return temp + 273.15
            
    elif from_unit == 'F':
        if to_unit == 'C':
            return (temp - 32) * 5/9
        elif to_unit == 'K':
            return (temp - 32) * 5/9 + 273.15
            
    elif from_unit == 'K':
        if to_unit == 'C':
            return temp - 273.15
        elif to_unit == 'F':
            return (temp - 273.15) * 9/5 + 32
            
    return temp  # Fallback    

def fetch_weather_data(city, unit='C'):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Convert temperature to the desired unit
        kelvin_temp = data['main']['temp']
        temp = convert_temperature(kelvin_temp - 273.15, 'C', unit)  # Convert from Kelvin to selected unit

        return {
            'city': city,
            'main': data['weather'][0]['main'],
            'temp': temp,
            'feels_like': convert_temperature(data['main']['feels_like'] - 273.15, 'C', unit),
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