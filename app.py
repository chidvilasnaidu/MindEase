import streamlit as st
from prompt_manager import SYSTEM_PROMPT
from gemini_client import generate_response
from memory_manager import (
    initialize_memory,
    update_memory,
    build_conversation_context,
)

st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🎯",
    layout="centered",
)

st.title("🎯 AI Career Advisor")
st.markdown("Professional Career Guidance with Context-Aware Intelligence")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = initialize_memory()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask your career-related question...")

if user_input:

    if len(user_input.strip()) < 5:
        st.warning("Please enter a more detailed question.")
        st.stop()

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Analyzing your profile..."):

        conversation_context = build_conversation_context(
            st.session_state.chat_history
        )

        full_prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{conversation_context}

User: {user_input}
"""

        assistant_response = generate_response(full_prompt)

    # Show assistant response only after full completion
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Update memory after rendering
    st.session_state.chat_history = update_memory(
        st.session_state.chat_history,
        user_input,
        assistant_response,
    )

st.divider()

if st.button("Clear Conversation"):
    st.session_state.chat_history = initialize_memory()
    st.rerun()