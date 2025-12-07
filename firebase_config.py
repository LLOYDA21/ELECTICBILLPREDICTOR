import pyrebase

firebase_config = {
    "apiKey": "AIzaSyDlAdCvxnS1SYyD5VWZTkANUp6l_R5xOYQ",
    "authDomain": "elective-cce20.firebaseapp.com",
    "projectId": "elective-cce20",
    "storageBucket": "elective-cce20.firebasestorage.app",
    "messagingSenderId": "345245765952",
    "appId": "1:345245765952:web:4e5607959c54e5496caaa5",
    "measurementId": "G-8B3MR8R9GF",
    
    # Pyrebase requirement (even if unused)
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
