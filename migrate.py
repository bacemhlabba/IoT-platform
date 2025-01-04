import sqlite3

DATABASE = 'local_database.db'

def migrate():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    # Add the timestamp column to the sensor_data table
    cur.execute("ALTER TABLE sensor_data ADD COLUMN timestamp TEXT")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()