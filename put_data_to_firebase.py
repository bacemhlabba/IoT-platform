import firebase_admin
from firebase_admin import credentials, db
import base64
import matplotlib.pyplot as plt
import numpy as np
import io

# Initialize Firebase
cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-project-53509-default-rtdb.europe-west1.firebasedatabase.app'
})

# Generate dynamic image
temperature = 25
humidity = 60
gas = 'normal'

# Create a half-circle plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
angles = np.linspace(0, np.pi, 100)
ax.plot(angles, np.ones_like(angles) * temperature, label='Temperature', color='blue')
ax.plot(angles, np.ones_like(angles) * humidity, label='Humidity', color='green')
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

print("Data added to Realtime Database successfully.")