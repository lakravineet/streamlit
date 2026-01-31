from firebase_config import db

users = [
    {
        "name": "Vineet Lakra",
        "Key":"1234"
        
    },
    {
        "name": "Rajath J",
        "Key":"5678"
    }
]

for q in users:
    db.collection("users").add(q)

print(f"{ len(users)} users added")
