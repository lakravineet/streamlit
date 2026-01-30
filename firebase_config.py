import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def init_firebase():
    """Initialize Firebase app and return Firestore client."""
    if not firebase_admin._apps:
        try:
            # Check if running on Streamlit Cloud
            if "firebase" in st.secrets:
                cred = credentials.Certificate(dict(st.secrets["firebase"]))
            # Local development with JSON file
            elif os.path.exists("serviceAccountKey.json"):
                cred = credentials.Certificate("serviceAccountKey.json")
            else:
                st.error("Firebase credentials not found!")
                st.stop()
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Failed to initialize Firebase: {str(e)}")
            st.stop()
    
    return firestore.client()

db = init_firebase()