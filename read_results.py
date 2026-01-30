import streamlit as st
from firebase_config import db
import pandas as pd
from tabulate import tabulate

results = db.collection("results").stream()

data = []
for r in results:
    row = r.to_dict()
    row["doc_id"] = r.id
    data.append(row)

df = pd.DataFrame(data)

#print(tabulate(df, headers="keys", tablefmt="psql"))

st.dataframe(df)

