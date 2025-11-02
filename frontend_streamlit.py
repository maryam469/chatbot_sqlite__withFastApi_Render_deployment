import streamlit as st
import requests

# ======================== CONFIG ===========================
API_URL = "https://chatbot-sqlite-withfastapi-render-28ep.onrender.com/"  # Your Render URL
# ===========================================================

st.set_page_config(page_title="LangGraph Chatbot 💬", layout="centered")
st.title("💬 LangGraph Chatbot (FastAPI + Streamlit)")

# ------------------ Session State Setup -------------------
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = None
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
if 'all_threads_history' not in st.session_state:
    st.session_state['all_threads_history'] = {}  # Stores messages per thread

# -------------------- Sidebar -----------------------------
st.sidebar.header("🧵 Chat Threads")

# Fetch existing threads from API
try:
    response = requests.get(f"{API_URL}/threads")
    if response.status_code == 200:
        threads = response.json().get("threads", [])
        for t in threads[::-1]:
            if st.sidebar.button(str(t)):
                st.session_state['thread_id'] = t
                # Load previous messages from session state
                st.session_state['message_history'] = st.session_state['all_threads_history'].get(t, [])
except Exception as e:
    st.sidebar.error("Error loading threads")

if st.sidebar.button("➕ New Chat"):
    st.session_state['thread_id'] = None
    st.session_state['message_history'] = []

# ------------------ Main Chat UI --------------------------
for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        payload = {
            "message": user_input,
            "thread_id": st.session_state["thread_id"]
        }
        response = requests.post(f"{API_URL}/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            ai_message = data["response"]
            st.session_state["thread_id"] = data["thread_id"]

            with st.chat_message("assistant"):
                st.markdown(ai_message)

            # Update message history
            st.session_state["message_history"].append(
                {"role": "assistant", "content": ai_message}
            )

            # Save current thread messages to all_threads_history
            if st.session_state["thread_id"]:
                st.session_state['all_threads_history'][st.session_state["thread_id"]] = st.session_state["message_history"]

        else:
            st.error("Backend error, please try again.")
    except Exception as e:
        st.error(f"Error: {e}")
