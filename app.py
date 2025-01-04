import sqlite3
from flask import Flask, render_template, request, jsonify
import subprocess
import firebase_admin
from firebase_admin import credentials, db
import base64
import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime

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
def home():
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
    if row is None:
        data = {'temperature': 'N/A', 'humidity': 'N/A', 'gas': 'N/A', 'led': 'N/A'}
    else:
        data = {
            'temperature': row['temperature'],
            'humidity': row['humidity'],
            'gas': row['gas'],
            'led': row['led']
        }
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

@app.route('/submit_data', methods=['POST'])
def submit_data():
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    gas = request.form['gas']

    # Generate dynamic image
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    angles = np.linspace(0, np.pi, 100)
    ax.plot(angles, np.ones_like(angles) * float(temperature), label='Temperature', color='blue')
    ax.plot(angles, np.ones_like(angles) * float(humidity), label='Humidity', color='green')
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(['0', '25', '50', '75', '100'])
    ax.set_title('Sensor Levels')
    ax.legend()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert image to base64
    encoded_string = base64.b64encode(buf.read()).decode('utf-8')

    # Add data to Realtime Database
    ref = db.reference('/sensor_data/latest')
    ref.set({
        'temperature': temperature,
        'humidity': humidity,
        'gas': gas,
        'image': encoded_string
    })

    return "Data added to Realtime Database successfully."

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        gas = request.form['gas']

        # Generate dynamic image
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        angles = np.linspace(0, np.pi, 100)
        ax.plot(angles, np.ones_like(angles) * float(temperature), label='Temperature', color='blue')
        ax.plot(angles, np.ones_like(angles) * float(humidity), label='Humidity', color='green')
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_yticklabels(['0', '25', '50', '75', '100'])
        ax.set_title('Sensor Levels')
        ax.legend()

        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Convert image to base64
        encoded_string = base64.b64encode(buf.read()).decode('utf-8')

        # Add data to Realtime Database
        ref = db.reference('/sensor_data/latest')
        ref.set({
            'temperature': temperature,
            'humidity': humidity,
            'gas': gas,
            'image': encoded_string
        })

        return jsonify({'status': 'success', 'message': 'Data submitted successfully'})

    return render_template('submit_form.html')

@app.route('/submit_sqlite', methods=['GET'])
def render_submit_sqlite():
    return render_template('submit_sqlite.html')

@app.route('/submit_sqlite', methods=['POST'])
def handle_submit_sqlite():
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    timestamp = request.form['timestamp']

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO sensor_data (temperature, humidity, gas, led, timestamp) VALUES (?, ?, ?, ?, ?)",
                (temperature, humidity, 'Normal', 'OFF', timestamp))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Data submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
