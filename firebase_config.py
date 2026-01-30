import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def init_firebase():
    if not firebase_admin._apps:

        if st.secrets.get("firebase", None):  # Streamlit Cloud
            cred = credentials.Certificate(dict(st.secrets["firebase"]))

        elif os.path.exists("serviceAccountKey.json"):  # Local
            cred = credentials.Certificate("serviceAccountKey.json")

        else:
            raise Exception("Firebase credentials not found")

        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()
