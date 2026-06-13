import streamlit as st

from services.pdf_reader import extract_text
from services.qa_engine import answer_question
from services.quiz_generator import generate_quiz
from services.summarizer import generate_summary


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

✅ Question Answering

✅ Quiz Generation
""")

st.title("🤖 AI Study Assistant")

st.markdown("""
### Personalized Study Assistant Using Generative AI

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
        st.error("No text found in PDF.")
        st.stop()

    st.success("PDF Uploaded Successfully 🎉")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AI Model", "Gemini")

    with col2:
        st.metric("Status", "Online")

    with col3:
        st.metric("Words Extracted", len(notes.split()))

    st.markdown("---")

    with st.expander("📖 View Extracted Notes"):
        st.write(notes[:5000])

    tab1, tab2, tab3 = st.tabs(
        [
            "📝 Summary",
            "❓ Q&A",
            "📚 Quiz"
        ]
    )

    with tab1:

        if st.button("🚀 Generate Summary"):

            with st.spinner("Generating Summary..."):
                summary = generate_summary(notes)

            st.write(summary)

            st.download_button(
                "📥 Download Summary",
                summary,
                file_name="summary.txt"
            )

    with tab2:

        question = st.text_input(
            "Ask a question from your notes"
        )

        if st.button("🤖 Get Answer"):

            if question:

                with st.spinner("Thinking..."):
                    answer = answer_question(
                        notes,
                        question
                    )

                st.write(answer)

            else:
                st.warning(
                    "Please enter a question."
                )

    with tab3:

        if st.button("📚 Generate Quiz"):

            with st.spinner("Creating Quiz..."):
                quiz = generate_quiz(notes)

            st.write(quiz)

            st.download_button(
                "📥 Download Quiz",
                quiz,
                file_name="quiz.txt"
            )

else:
    st.info("Upload a PDF to begin.")