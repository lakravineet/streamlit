from firebase_config import db

questions = [
    {
        "question": "What is Python?",
        "options": ["Snake", "Programming Language", "Car", "Game"],
        "answer": "Programming Language"
    },
    {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    }
]

for q in questions:
    db.collection("questions").add(q)

print("Questions added!")
