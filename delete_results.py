import streamlit as st
from firebase_config import db
import pandas as pd



results = db.collection("results").stream()

for r in results:
    data = r.to_dict()
    if data.get("score", 0) < 3:
        r.reference.delete()
        print("Deleted:", r.id)



st.subheader("🗑 Manage Results")

results = db.collection("results").stream()

data = []

for r in results:
    row = r.to_dict()
    row["doc_id"] = r.id   # attach id to row
    row["Delete?"] = False
    data.append(row)

if data:
    df = pd.DataFrame(data)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        disabled=["doc_id"]  # prevent editing id
    )

    if st.button("Delete Selected Rows"):
        rows_to_delete = edited_df[edited_df["Delete?"] == True]

        for doc_id in rows_to_delete["doc_id"]:
            db.collection("results").document(doc_id).delete()

        st.success(f"Deleted {len(rows_to_delete)} records")
        st.rerun()
else:
    st.write("No results found.")
