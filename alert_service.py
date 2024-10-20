import sqlite3

ALERT_THRESHOLDS = {'temp': 35}  # Default threshold for alerts (Celsius)

def configure_alerts(threshold_data):
    global ALERT_THRESHOLDS
    ALERT_THRESHOLDS.update(threshold_data)

def check_alerts():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT city, temp FROM weather 
                      WHERE dt > strftime('%s', 'now', '-10 minutes')''')
    alerts = []
    for city, temp in cursor.fetchall():
        if temp > ALERT_THRESHOLDS['temp']:
            alerts.append(f"Alert: {city} has exceeded {ALERT_THRESHOLDS['temp']}°C")
    conn.close()
    return alerts
