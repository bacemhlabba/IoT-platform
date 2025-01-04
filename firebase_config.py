import firebase_admin
from firebase_admin import credentials, firestore

# Firebase configuration details
cred = credentials.Certificate('path/to/your/firebase/credentials.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
