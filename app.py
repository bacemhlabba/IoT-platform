from flask import Flask, render_template, request, jsonify
import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)

# Firebase configuration
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    # Fetch data from Firebase
    doc_ref = db.collection('sensor_data').document('latest')
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
    else:
        data = {'temperature': 'N/A', 'humidity': 'N/A', 'gas': 'N/A'}
    return render_template('page1.html', data=data)

@app.route('/page2')
def page2():
    # Fetch data from local database
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    data = cur.fetchone()
    if data:
        data = dict(data)
    else:
        data = {'temperature': 'N/A', 'humidity': 'N/A', 'gas': 'N/A', 'led': 'N/A'}
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
