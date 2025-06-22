from unittest.mock import patch
import sqlite3
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Patch Firebase initialization before importing the app module
with patch('firebase_admin.initialize_app'), patch('firebase_admin.credentials.Certificate'):
    import app


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature TEXT,
        humidity TEXT,
        gas TEXT,
        led TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()


def test_update_led():
    fd, db_path = tempfile.mkstemp()
    os.close(fd)
    init_db(db_path)

    # Insert a single row
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO sensor_data (temperature, humidity, gas, led) VALUES (?, ?, ?, ?)",
        ("25", "60", "Normal", "OFF"),
    )
    conn.commit()
    conn.close()

    # Use temporary database in the app
    app.DATABASE = db_path
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        resp = client.post('/update_led', json={'led_state': 'ON'})
        assert resp.status_code == 200

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT led FROM sensor_data ORDER BY id DESC LIMIT 1")
    led = cur.fetchone()[0]
    conn.close()

    assert led == 'ON'
