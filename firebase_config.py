import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def init_firebase():
    if not firebase_admin._apps:

        # 🔹 CASE 1 — Running on Streamlit Cloud
        if "firebase" in st.secrets:
            cred = credentials.Certificate(dict(st.secrets["firebase"]))

        # 🔹 CASE 2 — Running locally
        elif os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")

        else:
            raise Exception("Firebase credentials not found")

        firebase_admin.initialize_app(cred)

    return firestore.client()


db = init_firebase()
