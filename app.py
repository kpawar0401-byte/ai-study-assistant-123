import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

st.markdown("""
<h1 style='text-align:center;'>🎓 AI Smart Study Assistant</h1>
<p style='text-align:center;'>Final Year Project | AI Powered Learning App</p>
""", unsafe_allow_html=True)


API_KEY = "AQ.Ab8RN6KZNP7vfDTpzUGiaKKSmSDhIglX40xQ8lcuNSerSAygOg"
genai.configure(api_key=API_KEY)


st.set_page_config(page_title="AI Study Assistant", page_icon="🎓")


theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "score" not in st.session_state:
    st.session_state.score = 0


with st.sidebar:
    st.title("🎓 AI Study Assistant")
    st.subheader("📚 Features")
    st.write("✅ AI Question Answer")
    st.write("🧠 MCQ Generator")
    st.write("📝 Notes Generator")
    st.write("❓ Important Questions")
    st.write("📄 PDF Download")
    st.write("🎯 Quiz Test")
    st.success("Ready!")


st.title("🎓 AI Study Assistant")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Chat",
    "PDF",
    "Quiz",
    "Dashboard",
    "Planner"
])

with tab1:
    st.subheader("💬 AI Chat")

    chat_input = st.text_input("Apna question likho", key="chat_input")

    if st.button("Send 💬"):
        if chat_input.strip() == "":
            st.warning("Kuch likho pehle")
        else:
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(chat_input)

                st.session_state.chat_history.append(("You", chat_input))
                st.session_state.chat_history.append(("AI", response.text))

                st.write("🤖 AI Answer:")
                st.write(response.text)

            except:
                st.error("API Error / Limit reached")

    st.subheader("💬 Chat History")

    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.write("🧑‍🎓 You: " + msg)
        else:
            st.write("🤖 AI: " + msg)

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []


with tab2:
    st.subheader("📄 Upload PDF")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    pdf_text = ""

    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() or ""
        st.success("PDF Loaded Successfully!")


def create_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [Paragraph(text, styles["Normal"])]
    doc.build(content)
    buffer.seek(0)
    return buffer


with tab3:
    st.subheader("🎯 Quiz")

    questions = [
        {
            "question": "What does CPU stand for?",
            "options": ["Central Processing Unit", "Computer Unit", "Control Unit"],
            "answer": "Central Processing Unit"
        },
        {
            "question": "HTML is used for?",
            "options": ["Web Pages", "Database", "OS"],
            "answer": "Web Pages"
        }
    ]

    score = 0

    for i, q in enumerate(questions):
        ans = st.radio(q["question"], q["options"], key=f"q_{i}")
        if ans == q["answer"]:
            score += 1

    if st.button("Submit Quiz"):
        st.session_state.score = score
        st.success(f"Score: {score}/{len(questions)}")


with tab4:
    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 Subjects", 4)

    with col2:
        st.metric("💬 Chats", len(st.session_state.chat_history))

    with col3:
        st.metric("🏆 Score", st.session_state.score)

with tab5:
    st.subheader("🤖 AI Study Planner")

    goal = st.text_input("Enter Goal")
    exam_date = st.date_input("Exam Date")

    if st.button("Generate Plan"):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(
                f"Create study plan for {goal} exam on {exam_date}"
            )
            st.write(response.text)
        except:
            st.error("API Error")