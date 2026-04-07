"""
main.py - Streamlit UI for MindEase Mental Health Support Chatbot.
"""

import streamlit as st
from config import GEMINI_API_KEY
from gemini_client import generate_response
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from session_manager import SessionManager

st.set_page_config(
    page_title="MindEase – Mental Health Support",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #f0f4f0 0%, #e8f0ee 50%, #f4f0f0 100%);
}
.mindease-header { text-align: center; padding: 2rem 0 1rem; }
.mindease-header h1 {
    font-family: 'Lora', serif; font-size: 2.4rem;
    color: #2d5a4e; margin: 0; letter-spacing: -0.5px;
}
.mindease-header p { color: #7a9e96; font-size: 0.95rem; font-weight: 300; margin-top: 0.3rem; }

.chat-user {
    background: #2d5a4e; color: #ffffff;
    padding: 0.85rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.5rem 0 0.5rem 20%;
    font-size: 0.95rem; line-height: 1.55;
    box-shadow: 0 2px 8px rgba(45,90,78,0.15);
}
.chat-bot {
    background: #ffffff; color: #2c3e35;
    padding: 0.85rem 1.1rem;
    border-radius: 18px 18px 18px 4px;
    margin: 0.5rem 20% 0.5rem 0;
    font-size: 0.95rem; line-height: 1.65;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-left: 3px solid #8bbcb0;
}
.chat-label {
    font-size: 0.75rem; font-weight: 500;
    letter-spacing: 0.05em; text-transform: uppercase;
    margin-bottom: 0.15rem; opacity: 0.6;
}
.chat-divider { border: none; border-top: 1px solid #d9e8e4; margin: 1.5rem 0; }

.stTextInput > div > div > input {
    border-radius: 24px !important; border: 2px solid #c5ddd7 !important;
    padding: 0.7rem 1.2rem !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important; background: #ffffff !important; color: #2c3e35 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2d5a4e !important;
    box-shadow: 0 0 0 3px rgba(45,90,78,0.1) !important;
}
.stButton > button {
    border-radius: 24px !important; background: #2d5a4e !important;
    color: white !important; border: none !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover { background: #1e3d35 !important; }
section[data-testid="stSidebar"] { background: #f7faf9; }
.crisis-banner {
    background: #fff3f3; border-left: 4px solid #e57373;
    border-radius: 8px; padding: 0.7rem 1rem; margin: 1rem 0;
    font-size: 0.88rem; color: #c0392b;
}
</style>
""", unsafe_allow_html=True)


def _init_state():
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = SessionManager()
    if "display_history" not in st.session_state:
        st.session_state.display_history = []


_init_state()

st.markdown("""
<div class="mindease-header">
    <h1>🌿 MindEase</h1>
    <p>A safe space to talk • Compassionate AI support • Always here for you</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="crisis-banner">
    🆘 <strong>In crisis?</strong> Call iCall: <strong>9152987821</strong>
    &nbsp;|&nbsp; Emergency: <strong>112</strong>
    &nbsp;|&nbsp; International: <a href="https://befrienders.org" target="_blank">befrienders.org</a>
</div>
""", unsafe_allow_html=True)

if not st.session_state.display_history:
    st.markdown(
        f'<div class="chat-bot"><div class="chat-label">MindEase</div>{WELCOME_MESSAGE}</div>',
        unsafe_allow_html=True
    )

for role, text in st.session_state.display_history:
    if role == "user":
        st.markdown(f'<div class="chat-user"><div class="chat-label">You</div>{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot"><div class="chat-label">MindEase</div>{text}</div>', unsafe_allow_html=True)

st.markdown('<hr class="chat-divider">', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        label="Message",
        placeholder="Share what's on your mind…",
        label_visibility="collapsed",
        key="user_input_field",
    )
with col2:
    send_btn = st.button("Send", use_container_width=True)

if send_btn and user_input.strip():
    message = user_input.strip()
    st.session_state.display_history.append(("user", message))

    sm: SessionManager = st.session_state.session_manager
    sm.add_user_message(message)

    with st.spinner("MindEase is thinking…"):
        # Build full prompt as plain string — same as friend's pattern
        conversation_context = sm.build_context()
        full_prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{conversation_context}

User: {message}
"""
        response_text = generate_response(full_prompt, user_message=message)

    sm.add_model_message(response_text)
    st.session_state.display_history.append(("bot", response_text))
    st.rerun()

with st.sidebar:
    st.markdown("### 🌿 About MindEase")
    st.markdown(
        "MindEase is an AI-powered mental health support companion. "
        "It provides empathetic conversation and evidence-based coping strategies.\n\n"
        "**It is not a substitute for professional therapy.**"
    )
    st.divider()
    sm_ref: SessionManager = st.session_state.session_manager
    st.metric("Conversation Turns", sm_ref.turn_count)
    st.divider()
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.session_manager.clear()
        st.session_state.display_history = []
        st.rerun()
    st.divider()
    st.markdown("**Crisis Resources**")
    st.markdown("- iCall: 9152987821\n- Vandrevala: 1860-2662-345\n- [befrienders.org](https://befrienders.org)")
