import sqlite3

def setup_db():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT,
                        main TEXT,
                        temp REAL,
                        feels_like REAL,
                        dt INTEGER
                      )''')
    conn.commit()
    conn.close()
