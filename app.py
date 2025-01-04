from flask import Flask, render_template, request, jsonify
import sqlite3
import firebase_admin
from firebase_admin import credentials, db
import os

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-project-53509-default-rtdb.europe-west1.firebasedatabase.app'
})

# SQLite configuration
DATABASE = 'local_database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def page1():
    # Fetch data from Firebase Realtime Database
    ref = db.reference('/sensor_data/latest')
    data = ref.get()
    if data is None:
        data = {'temperature': 'N/A', 'humidity': 'N/A', 'gas': 'N/A', 'image': ''}
    return render_template('page1.html', data=data)

@app.route('/page2')
def page2():
    # Fetch data from local database
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    data = {'temperature': row['temperature'], 'humidity': row['humidity'], 'gas': row['gas'], 'led': row['led']} if row else {'temperature': 'N/A', 'humidity': 'N/A', 'gas': 'N/A', 'led': 'N/A'}
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data)
    return render_template('page2.html', data=data)

@app.route('/update_led', methods=['POST'])
def update_led():
    led_state = request.json.get('led_state')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE sensor_data SET led = ? WHERE id = (SELECT MAX(id) FROM sensor_data)", (led_state,))
    conn.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
