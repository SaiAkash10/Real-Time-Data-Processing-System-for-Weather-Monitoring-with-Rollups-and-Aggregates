import os
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
import sqlite3

def generate_temp_trend(city):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT dt, temp FROM weather WHERE city=? ORDER BY dt ASC''', (city,))
    data = cursor.fetchall()
    conn.close()

    if not data:
        return None  # Handle case where no data is found

    timestamps = [entry[0] for entry in data]
    temperatures = [entry[1] for entry in data]

    plt.plot(timestamps, temperatures, label=f'Temperature in {city}')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Temperature Trend for {city}')
    plt.legend()

    # Save the image to the static directory
    image_path = os.path.join('static', f'{city}_temp_trend.png')
    plt.savefig(image_path)
    plt.close()

    return image_path  # Return the path to the saved image
