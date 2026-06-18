import streamlit as st
import time
import re

from services.pdf_reader import extract_text
from services.qa_engine import answer_question
from services.quiz_generator import generate_quiz
from services.summarizer import generate_summary
from utils.quiz_parser import parse_quiz
from utils.db_manager import initialize_database, save_documnet_to_db, get_user_data

# ── Initialize DB tables on every startup (safe — uses CREATE IF NOT EXISTS) ──
initialize_database()

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🚀",
    layout="wide"
)

# ── Track stats in session state ──────────────────────────────────────────────
for key, default in [
    ("pdfs_uploaded", 0),
    ("questions_asked", 0),
    ("quizzes_taken", 0),
    ("avg_score", 0),
    ("score_history", []),
    ("messages", []),
    ("last_uploaded_filename", None),
    ("notes", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
[data-testid="stAppViewContainer"] { background: #0d1117 !important; }
[data-testid="stHeader"]           { background: #0d1117 !important; }
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1rem; }
.sidebar-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 1.5rem; }
.sidebar-logo-icon {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px; width: 38px; height: 38px;
    display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.sidebar-logo-text { font-size: 15px; font-weight: 700; color: white; }
.sidebar-badge {
    padding: 10px 14px; border-radius: 10px; font-size: 13px; font-weight: 600;
    display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}
.badge-blue  { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); }
.badge-teal  { background: rgba(20,184,166,0.12); color: #2dd4bf; border: 1px solid rgba(20,184,166,0.25); }
.features-section { margin-top: 1.5rem; }
.features-title { font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
.feature-item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #d1d5db; padding: 7px 0; }
.feature-check {
    width: 20px; height: 20px; border-radius: 6px;
    background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3);
    display: flex; align-items: center; justify-content: center; font-size: 11px; flex-shrink: 0;
}
.sidebar-bottom-card {
    margin-top: 2rem; background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2); border-radius: 12px; padding: 14px;
}
.sidebar-bottom-card .card-title { font-size: 13px; font-weight: 700; color: white; display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.sidebar-bottom-card .card-sub   { font-size: 12px; color: #6b7280; }
.sidebar-bottom-card .card-sub span { color: #818cf8; }
.hero { text-align: center; padding: 2.5rem 1rem 1.5rem; }
.hero-title { font-size: 52px; font-weight: 800; color: white; margin: 0 0 12px; line-height: 1.15; }
.hero-tagline { font-size: 18px; font-weight: 600; color: white; margin-bottom: 10px; }
.hero-tagline .dot { color: #6366f1; margin: 0 8px; }
.hero-sub { font-size: 15px; color: #6b7280; margin-bottom: 0; }
.upload-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px; padding: 2rem 2rem 1.5rem; margin: 1.5rem 0; text-align: center;
}
.upload-icon   { font-size: 42px; margin-bottom: 10px; }
.upload-title  { font-size: 24px; font-weight: 700; color: white; margin-bottom: 8px; }
.upload-desc   { font-size: 14px; color: #6b7280; margin-bottom: 1.5rem; }
.stats-row { display: flex; gap: 16px; margin-top: 1.5rem; }
.stat-card {
    flex: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 18px 16px; display: flex; align-items: center; gap: 14px;
}
.stat-icon { font-size: 24px; }
.stat-num  { font-size: 26px; font-weight: 800; color: white; line-height: 1; }
.stat-label{ font-size: 12px; color: #6b7280; margin-top: 3px; }
.info-cards-row { display: flex; gap: 14px; margin: 1rem 0; }
.info-card {
    flex: 1; background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2); border-radius: 12px; padding: 14px 16px;
}
.info-card .ic-label { font-size: 11px; color: #6b7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.info-card .ic-value { font-size: 18px; font-weight: 700; color: white; margin-top: 4px; }
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important; border-radius: 12px !important;
    padding: 4px !important; gap: 4px !important; border: 1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; font-size: 14px !important;
    font-weight: 600 !important; color: #6b7280 !important; padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] { background: rgba(99,102,241,0.2) !important; color: #818cf8 !important; }
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-weight: 700 !important; font-size: 15px !important; padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    opacity: 0.9 !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(99,102,241,0.3) !important;
}
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed rgba(99,102,241,0.35) !important;
    border-radius: 14px !important; padding: 12px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,0.6) !important;
    background: rgba(99,102,241,0.04) !important;
}
.stSuccess { background: rgba(34,197,94,0.1) !important; border: 1px solid rgba(34,197,94,0.25) !important; border-radius: 10px !important; color: #4ade80 !important; }
.stInfo    { background: rgba(99,102,241,0.1) !important; border: 1px solid rgba(99,102,241,0.25) !important; border-radius: 10px !important; color: #818cf8 !important; }
.stError   { background: rgba(239,68,68,0.1) !important; border: 1px solid rgba(239,68,68,0.25) !important; border-radius: 10px !important; }
.stRadio > div { gap: 12px !important; }
.stRadio label {
    background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; padding: 8px 16px !important; color: #d1d5db !important;
    font-size: 14px !important; cursor: pointer !important;
}
[data-testid="stExpander"] { background: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 12px !important; }
[data-testid="stExpander"] summary { color: #d1d5db !important; font-weight: 600 !important; }
[data-testid="stChatMessage"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 14px !important; margin-bottom: 10px !important; }
[data-testid="stChatInput"]   { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(99,102,241,0.3) !important; border-radius: 12px !important; color: white !important; }
.stProgress > div > div { background: linear-gradient(90deg, #6366f1, #8b5cf6) !important; border-radius: 99px !important; }
.stProgress { background: rgba(255,255,255,0.06) !important; border-radius: 99px !important; }
hr { border-color: rgba(255,255,255,0.07) !important; }
.stCaption, footer { color: #374151 !important; text-align: center; }
p, li, span, label, .stMarkdown { color: #d1d5db !important; }
h1, h2, h3, h4 { color: white !important; }
.block-container { padding-top: 0 !important; max-width: 1100px !important; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">📚</div>
        <div class="sidebar-logo-text">AI Study Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-badge badge-blue">🎓 &nbsp; Summer Project 2026</div>
    <div class="sidebar-badge badge-teal">🤖 &nbsp; AI-Powered</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="features-section">
        <div class="features-title">Features</div>
        <div class="feature-item"><div class="feature-check">✓</div> PDF Upload</div>
        <div class="feature-item"><div class="feature-check">✓</div> Smart Summary</div>
        <div class="feature-item"><div class="feature-check">✓</div> RAG-Based Q&amp;A</div>
        <div class="feature-item"><div class="feature-check">✓</div> Quiz Generation</div>
        <div class="feature-item"><div class="feature-check">✓</div> Web Search</div>
        <div class="feature-item"><div class="feature-check">✓</div> Hybrid Search</div>
        <div class="feature-item"><div class="feature-check">✓</div> Score Analytics</div>
    </div>
    <div class="sidebar-bottom-card">
        <div class="card-title">✦ AI-Powered Learning</div>
        <div class="card-sub">Learn Faster. <span>Revise Smarter.</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🗄️ Your AI Knowledge Vault")
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

    # ── FIX: get_user_data() is now safe even with no summaries cached ──
    library_items = get_user_data()
    if library_items:
        for n in library_items:
            with st.expander(f"📑 {n['filename']}"):
                # ── FIX: correct key name ──
                st.caption(f"📅 Uploaded: {n['Upload_date']}")
                st.markdown("**📌 AI Summary preview:**")
                st.write(n["summary"])
                if st.button("Load Text", key=f"side_load_{n['id']}"):
                    st.session_state.last_uploaded_filename = n["filename"]
                    st.session_state.notes = n["processed_text"]
                    st.success(f"Loaded {n['filename']}!")
    else:
        # ── FIX: else is outside the for loop now ──
        st.info("Your vault is empty. Drop a PDF in the main panel to start your collection!")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-title">🚀 AI Study Assistant</div>
    <div class="hero-tagline">
        Learn Faster <span class="dot">•</span> Revise Smarter <span class="dot">•</span> Score Higher
    </div>
    <div class="hero-sub">AI-Powered Study Companion using RAG, Web Search and LLMs</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# UPLOAD CARD
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="upload-card">
    <div class="upload-icon">☁️</div>
    <div class="upload-title">Upload PDF Notes</div>
    <div class="upload-desc">
        Upload your PDF study notes and let AI summarize,<br>answer questions and generate quizzes.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag and drop file here · Limit 200MB per file · PDF",
    type=["pdf"],
    label_visibility="visible"
)


# ═══════════════════════════════════════════════════════════════════════════════
# STATS ROW
# ═══════════════════════════════════════════════════════════════════════════════
stats_placeholder = st.empty()


def render_stats():
    stats_placeholder.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-icon">📄</div>
        <div>
            <div class="stat-num">{st.session_state.pdfs_uploaded}</div>
            <div class="stat-label">PDFs Uploaded</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div>
            <div class="stat-num">{st.session_state.questions_asked}</div>
            <div class="stat-label">Questions Asked</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div>
            <div class="stat-num">{st.session_state.quizzes_taken}</div>
            <div class="stat-label">Quizzes Taken</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🏆</div>
        <div>
            <div class="stat-num">{st.session_state.avg_score}%</div>
            <div class="stat-label">Avg Score</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# AFTER PDF UPLOAD
# ═══════════════════════════════════════════════════════════════════════════════
if uploaded_file:

    with st.spinner("Reading PDF..."):
        notes = extract_text(uploaded_file)

    if not notes or not notes.strip():
        st.error("❌ No text found in this PDF. Please try another file.")
        st.stop()

    # ── FIX: store notes in session state so tabs can always access it ──
    st.session_state.notes = notes

    # Save to DB (safe — skips if already saved)
    save_documnet_to_db(uploaded_file.name, notes)

    # Count only new uploads
    if uploaded_file.name != st.session_state.last_uploaded_filename:
        st.session_state.pdfs_uploaded += 1
        st.session_state.last_uploaded_filename = uploaded_file.name
        st.session_state.messages = []

    st.success("✅ PDF uploaded and synchronized successfully!")

    st.markdown(f"""
    <div class="info-cards-row">
        <div class="info-card">
            <div class="ic-label">🤖 AI Model</div>
            <div class="ic-value">Gemini</div>
        </div>
        <div class="info-card">
            <div class="ic-label">🔍 Search Mode</div>
            <div class="ic-value">RAG + Web</div>
        </div>
        <div class="info-card">
            <div class="ic-label">📄 Words Extracted</div>
            <div class="ic-value">{len(notes.split()):,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 View Extracted Notes"):
        st.write(notes[:5000])

    search_mode = st.radio(
        "Search Mode",
        ["🚀 Hybrid", "📄 PDF Only", "🌐 Web Only"],
        horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📝 Summary", "❓ Q&A", "📚 Quiz"])

    # ── Tab 1: Summary ────────────────────────────────────────────────────────
    with tab1:
        if st.button("🚀 Generate Summary"):
            with st.spinner("Generating Summary with anti-hallucination guardrails..."):
                summary = generate_summary(notes)
            st.session_state["summary_text"] = summary

        if st.session_state.get("summary_text"):
            placeholder = st.empty()
            typed_text = ""
            for char in st.session_state["summary_text"]:
                typed_text += char
                placeholder.markdown(f"""
<div style="
    padding: 20px; border-radius: 14px;
    border: 1px solid rgba(99,102,241,0.2);
    background: rgba(99,102,241,0.05);
    color: #d1d5db; line-height: 1.7;
">
{typed_text}
</div>
""", unsafe_allow_html=True)
                time.sleep(0.001)
            st.download_button(
                "📥 Download Summary",
                st.session_state["summary_text"],
                file_name="summary.txt"
            )

    # ── Tab 2: Q&A ───────────────────────────────────────────────────────────
    with tab2:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask anything from your notes…")
        if question:
            st.session_state.questions_asked += 1
            render_stats()
            st.session_state.messages.append({"role": "user", "content": question})

            with st.chat_message("user", avatar="🧑‍🎓"):
                st.write(question)

            with st.spinner("Searching notes…"):
                answer = answer_question(uploaded_file, question, search_mode)

            with st.chat_message("assistant", avatar="🤖"):
                placeholder = st.empty()
                typed_text = ""
                tokens = re.split(r'(\s+)', answer)
                for token in tokens:
                    typed_text += token
                    placeholder.text(typed_text + "▌")
                    if token.strip():
                        time.sleep(0.03)
                placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    # ── Tab 3: Quiz ───────────────────────────────────────────────────────────
    with tab3:
        if st.button("📚 Generate Quiz"):
            with st.spinner("Creating a structured quiz…"):
                quiz = generate_quiz(notes, num_questions=10)
                st.session_state["quiz"] = quiz

        if st.session_state.get("quiz"):
            questions = parse_quiz(st.session_state["quiz"])

            if questions:
                st.subheader("🎯 Quiz")
                answers = {}

                for i, q in enumerate(questions):
                    st.markdown(f"""
<div style="
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 16px 18px; margin-bottom: 12px;
">
<p style="color:#818cf8;font-size:12px;font-weight:700;text-transform:uppercase;margin:0 0 6px;">Question {i+1}</p>
<p style="color:white;font-size:15px;margin:0;">{q["question"]}</p>
</div>
""", unsafe_allow_html=True)
                    answers[i] = st.radio(
                        "Choose your answer",
                        q["options"],
                        index=None,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )

                if st.button("🚀 Submit Quiz"):
                    score = 0
                    for i, q in enumerate(questions):
                        selected = st.session_state.get(f"q_{i}")
                        correct = q["answer"]

                        st.markdown(f"#### Question {i+1}")
                        st.write("Selected →", selected)
                        st.write("Correct →", correct)

                        if selected and selected.startswith(correct):
                            score += 1
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Wrong — Correct Answer: {correct}")

                        st.info(q["explanation"])

                    # ── FIX: stats update AFTER the loop, not inside it ──
                    percentage = int((score / len(questions)) * 100) if questions else 0
                    st.session_state.quizzes_taken += 1
                    st.session_state.score_history.append(percentage)
                    st.session_state.avg_score = int(
                        sum(st.session_state.score_history) / len(st.session_state.score_history)
                    )
                    render_stats()

                    st.markdown(f"""
<div style="
    padding: 30px; border-radius: 16px; text-align: center;
    background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.25);
    margin-top: 16px;
">
<p style="font-size:28px;margin:0;">🏆</p>
<h2 style="color:white;margin:8px 0 4px;">Quiz Results</h2>
<p style="font-size:42px;font-weight:800;color:#818cf8;margin:0;">{score}/{len(questions)}</p>
<p style="font-size:20px;color:#d1d5db;margin:4px 0 0;">{percentage}% Score</p>
</div>
""", unsafe_allow_html=True)

                    st.progress(percentage / 100)
                    st.download_button(
                        "📥 Download Quiz",
                        st.session_state["quiz"],
                        file_name="quiz.txt"
                    )
            else:
                st.warning("⚠️ Could not parse quiz questions. Try generating again.")

else:
    st.markdown("""
<div style="text-align: center; padding: 2rem; color: #4b5563; font-size: 15px;">
    ⬆️ Upload a PDF above to get started.
</div>
""", unsafe_allow_html=True)


# ── Render stats with final up-to-date values ──────────────────────────────────
render_stats()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Developed by Himanshu Rawat and Aditya Badatya | AI Study Assistant")
