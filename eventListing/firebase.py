import firebase_admin
from firebase_admin import credentials

# Replace 'path/to/serviceAccountKey.json' with the path to your service account key JSON file
cred = credentials.Certificate('/home/chicmic/Documents/python/eventListing/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
