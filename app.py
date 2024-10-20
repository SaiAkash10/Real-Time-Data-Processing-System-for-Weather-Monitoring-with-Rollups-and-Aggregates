from flask import Flask, render_template, request, redirect, url_for, jsonify
from weather_service import fetch_and_store_weather, get_daily_summary, fetch_weather_data, store_weather_data, CITIES, display_weather_info
from visualization import generate_temp_trend
from alert_service import check_alerts, configure_alerts
from models import setup_db
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
import sqlite3
import threading
import time
import os

app = Flask(__name__)

# Setup database
setup_db()

# Function to periodically fetch weather data
def schedule_weather_updates():
    while True:
        fetch_and_store_weather()
        check_alerts()
        time.sleep(300)  # Fetch every 5 minutes

@app.route('/')
def dashboard():
    daily_summary = get_daily_summary()  # Ensure this returns a list
    if daily_summary is None:
        daily_summary = []  # Fallback to an empty list
    return render_template('dashboard.html', summary=daily_summary)

@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    if request.method == 'POST':
        threshold_data = request.json
        configure_alerts(threshold_data)
        return jsonify({'message': 'Alert thresholds updated!'})
    alerts = check_alerts()
    return render_template('alerts.html', alerts=alerts)

@app.route('/settings', methods=['POST'])
def settings():
    global units  # Declare units as global to modify it
    units = request.form.get('Temp')  # This should get the selected temperature unit
    print(units)  
    return redirect(url_for('dashboard'))

def fetch_and_store_weather():
    for city in CITIES:
        weather_data = fetch_weather_data(city)  # Ensure the selected unit is passed here
        if weather_data:
            store_weather_data(city, weather_data)


# Route to handle the form submission and redirect to the visualization route
@app.route('/visualization', methods=['POST'])
def visualization():
    city = request.form.get('city')
    return redirect(url_for('visualize', city=city))

@app.route('/visualization/<city>')
def visualize(city):
    # Generate temperature trend chart
    image_path = generate_temp_trend(city)
    
    if image_path is None or not os.path.exists(image_path):
        return "Error: No data available or failed to generate visualization for the selected city."
    
    # Instead of sending the file, just render the visualization page
    return render_template('visualization.html', city=city)


if __name__ == '__main__':
    threading.Thread(target=schedule_weather_updates).start()
    app.run(debug=True, use_reloader=False)
