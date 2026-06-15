import streamlit as st
import time
import re

from services.pdf_reader import extract_text
from services.qa_engine import answer_question
from services.quiz_generator import generate_quiz
from services.summarizer import generate_summary
from utils.quiz_parser import (
    parse_quiz
)
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

h1 {
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.title("📚 AI Study Assistant")

    st.markdown("---")

    st.info("Summer Project 2026")

    st.success("Powered by Gemini AI")

    st.markdown("---")

    st.markdown("""
### Features

✅ PDF Upload

✅ Smart Summary

✅ RAG-Based Question Answering

✅ Quiz Generation

✅ Page Citations
""")

st.title("🤖 AI Study Assistant")

st.markdown("""
### Personalized Learning Using Generative AI + RAG

Upload your notes and let AI help you study smarter.
""")

uploaded_file = st.file_uploader(
    "📄 Upload PDF Notes",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Reading PDF..."):
        notes = extract_text(uploaded_file)

    if not notes:

        st.error(
            "No text found in PDF."
        )

        st.stop()

    st.success(
        "PDF Uploaded Successfully 🎉"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "AI Model",
            "Gemini"
        )

    with col2:
        st.metric(
            "Search",
            "RAG"
        )

    with col3:
        st.metric(
            "Words Extracted",
            len(notes.split())
        )

    st.markdown("---")

    with st.expander(
        "📖 View Extracted Notes"
    ):
        st.write(
            notes[:5000]
        )
    search_mode = st.radio(
        "Search Mode",
        [
            "🚀 Hybrid",
            "📄 PDF Only",
            "🌐 Web Only"
        ],
        horizontal=True)

    tab1, tab2, tab3 = st.tabs(
        [
            "📝 Summary",
            "❓ Q&A",
            "📚 Quiz"
        ]
    )

    with tab1:

        if st.button(
            "🚀 Generate Summary"
        ):

            with st.spinner(
                "Generating Summary..."
            ):

                summary = generate_summary(
                    notes
                )

            placeholder = st.empty()

            typed_text = ""

            for char in summary:
                typed_text += char
                placeholder.markdown(
                    typed_text
                )

            time.sleep(0.001)

            st.download_button(
                "📥 Download Summary",
                summary,
                file_name="summary.txt"
            )

    with tab2:

        question = st.text_input(
            "Ask a question from your notes"
        )

        if st.button(
            "🤖 Get Answer"
        ):

            if question:

                with st.spinner(
                    "Searching Notes..."
                ):

                    answer = answer_question(
                        uploaded_file,
                        question,
                        search_mode
                    )

                placeholder = st.empty()

                typed_text = ""

                import time

                for word in answer.split():

                    typed_text += word + " "

                    placeholder.markdown(
                        typed_text
                    )

                    time.sleep(0.03)

            else:

                st.warning(
                    "Please enter a question."
                )

    with tab3:

        if st.button(
            "📚 Generate Quiz"
        ):

            with st.spinner(
                "Creating Quiz..."
            ):

                quiz = generate_quiz(
                    notes
                )

                st.session_state["quiz"] = quiz
        if "quiz" in st.session_state:

            questions = parse_quiz(
                st.session_state["quiz"]
            )

            if questions:

                st.subheader(
                    "🎯 Quiz"
                )

                answers = {}

                for i, q in enumerate(questions):

                    st.markdown(
                        f"### Question {i+1}"
                    )

                    st.write(
                        q["question"]
                    )

                    answers[i] = st.radio(
                        "Choose your answer",
                        q["options"],
                        index=None,
                        key=f"q_{i}"
                    )

                if st.button(
                    "🚀 Submit Quiz"
                ):

                    score = 0

                    for i, q in enumerate(
                        questions
                    ):

                        selected = answers[i]

                        correct = q["answer"]

                        st.markdown(
                            f"## Question {i+1}"
                        )
                        st.write("Selected =", selected)
                        st.write("Correct =", correct)
                        if (
                            selected
                            and selected.startswith(
                                correct
                            )
                        ):

                            score += 1

                            st.success(
                                "✅ Correct"
                            )

                        else:

                            st.error(
                                f"❌ Wrong | Correct Answer: {correct}"
                            )

                        st.info(
                            q["explanation"]
                        )

                    st.success(
                        f"🏆 Final Score: {score}/{len(questions)}"
                    )

                    st.download_button(
                        "📥 Download Quiz",
                        st.session_state["quiz"],
                        file_name="quiz.txt"
                    )

else:
    st.info(
        "Upload a PDF to begin."
    )

st.markdown("---")

st.caption(
    "Developed by Himanshu Rawat | AI Study Assistant"
)