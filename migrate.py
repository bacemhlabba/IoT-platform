import sqlite3

DATABASE = 'local_database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature TEXT,
                    humidity TEXT,
                    gas TEXT,
                    led TEXT,
                    timestamp TEXT)''')
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO sensor_data (temperature, humidity, gas, led) VALUES ('25', '60', 'Normal', 'OFF')")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    insert_data()
