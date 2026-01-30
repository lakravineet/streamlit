import pyrebase

firebase_config = {
    "apiKey": "AIzaSyAFY4EQFONCtwDYMIy6aKAI_B7BVptERIc",
    "authDomain": "exam-portal-c68ac.firebaseapp.com",
    "projectId": "exam-portal-c68ac",
    "storageBucket":"exam-portal-c68ac.firebasestorage.app",
    "messagingSenderId": "118695787269",
    "appId": "1:118695787269:web:2eec26c8cd54f244d5156c",
    "databaseURL": ""
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()