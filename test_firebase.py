import streamlit as st
from firebase_config import db

docs = db.collection("results").stream()

all_data = []
for doc in docs:
    data = doc.to_dict()
    data["doc_id"] = doc.id   # optional: keep document ID
    all_data.append(data)

st.write(all_data)

for doc in db.collection("results").stream():
    print(f"ID: {doc.id}")
    print(f"Data: {doc.to_dict()}")
    print(f"Created: {doc.create_time}")
    print(f"Field 'score': {doc.get('score')}")
    print(f"Exists: {doc.exists}")
    print("---")

