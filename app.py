import streamlit as st
from firebase_config import db
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Exam Portal", layout="wide")

st.markdown("<h3 style='text-align:center;'>Examination Portal</h3>", unsafe_allow_html=True)

# Hide Streamlit UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

EXAM_MINUTES = 1

# -------- CACHE QUESTIONS --------
@st.cache_data(show_spinner=False)
def load_questions():
    docs = db.collection("questions").stream()
    questions = []
    for d in docs:
        q = d.to_dict()
        q["id"] = d.id
        questions.append(q)
    return questions

# -------- SESSION --------
if "user" not in st.session_state:
    st.session_state.user = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "view" not in st.session_state:
    st.session_state.view = "test"
if "saved" not in st.session_state:
    st.session_state.saved = False

# -------- SIMPLE LOGIN --------
# -------- KEY ONLY LOGIN --------
# -------- FIREBASE KEY LOGIN (REUSABLE) --------
# -------- FIREBASE KEY LOGIN (FIELD-BASED) --------
if not st.session_state.user:
    st.title("Login")

    entered_key = st.text_input("Enter Your Access Key")

    if st.button("Login"):

        docs = db.collection("users").where("Key", "==", entered_key).stream()
        user_doc = None

        for d in docs:
            user_doc = d.to_dict()
            break

        if not user_doc:
            st.error("Invalid access key")
            st.stop()

        st.session_state.user = {
            "name": user_doc["name"],
            "exam_key": entered_key,
            "localId": entered_key
        }

        st.rerun()

    st.stop()




# -------- SIDEBAR --------
st.sidebar.write(f"Welcome, {st.session_state.user['name']}")
#st.sidebar.write(f"📧 {st.session_state.user['email']}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# -------- START TEST --------
st.title("📝 Online Test")

if st.session_state.start_time is None:
    if st.button("Start Test"):
        st.session_state.start_time = datetime.now()
        st.rerun()

# -------- TIMER --------
placeholder = st.empty()

if st.session_state.start_time and st.session_state.view == "test":
    st_autorefresh(interval=1000, key="timer")

    end_time = st.session_state.start_time + timedelta(minutes=EXAM_MINUTES)
    seconds = int((end_time - datetime.now()).total_seconds())

    if seconds <= 0:
        st.session_state.view = "result"
        st.rerun()

    placeholder.warning(f"⏳ Time left: {seconds} sec")

# -------- QUESTIONS --------
if st.session_state.start_time and st.session_state.view == "test":

    questions = load_questions()

    for i, q in enumerate(questions):
        ans = st.radio(
            f"Q{i+1}. {q['question']}",
            q["options"],
            key=f"q{i}"
        )
        st.session_state.answers[q["id"]] = ans

    if st.button("Submit Test"):
        st.session_state.view = "result"
        st.rerun()

# -------- RESULT --------
if st.session_state.view == "result":

    questions = load_questions()
    score = 0
    total = len(questions)

    for q in questions:
        if st.session_state.answers.get(q["id"]) == q["answer"]:
            score += 1

    st.success(f"Test Finished! Your Score: {score}/{total}")
    #st.balloons()

    if not st.session_state.saved:
        db.collection("results").add({
            #"email": st.session_state.user["email"],
            "name": st.session_state.user["name"],
            "uid": st.session_state.user["localId"],
            "score": score,
            "total": total,
            "time": datetime.now()
        })
        st.session_state.saved = True

    if st.button("Return to Login"):
        st.session_state.clear()
        st.rerun()

    st.stop()
