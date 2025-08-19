import streamlit as st
import requests
import time

st.set_page_config(
    page_title="DataMinds Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💅🏼",
)

# Set background image via CSS
st.markdown(
    """
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1581092795360-1f6a7d0f1652');
        background-size: cover;
        background-attachment: fixed;
    }
    .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.9);
    }
    .chat-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .user-msg {
        background-color: #cce5ff;
        padding: 8px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .bot-msg {
        background-color: #d4edda;
        padding: 8px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize chat sessions
if "sessions" not in st.session_state:
    st.session_state.sessions = {"Default": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default"
if "bot_thinking" not in st.session_state:
    st.session_state.bot_thinking = False

# Sidebar: session selection and chat history
with st.sidebar:
    st.markdown("<h2>Chat Sessions</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Session selector
    session_names = list(st.session_state.sessions.keys())
    selected_session = st.selectbox("Select session", session_names)
    st.session_state.current_session = selected_session

    # Button to create new session
    if st.button("➕ New Chat"):
        new_name = f"Chat {len(st.session_state.sessions)+1}"
        st.session_state.sessions[new_name] = []
        st.session_state.current_session = new_name

    st.markdown("---")
    # Display chat history
    st.markdown("<h3>History</h3>", unsafe_allow_html=True)
    for msg in st.session_state.sessions[st.session_state.current_session]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'><b>Bot:</b> {msg['content']}</div>", unsafe_allow_html=True)

# Main chat input
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    # Add user message to current session
    st.session_state.sessions[st.session_state.current_session].append(
        {"role": "user", "content": user_input}
    )
    
    # Show thinking emoji
    st.session_state.bot_thinking = True
    placeholder = st.empty()
    placeholder.markdown("🤔 Bot is thinking...")

    # Send message to backend
    response = requests.post(
        "http://backend:8000/chat", json={"message": user_input}, stream=True
    )
    
    # Collect streamed response
    bot_reply = ""
    for chunk in response.iter_lines():
        if chunk:
            text_chunk = chunk.decode()
            bot_reply += text_chunk
            placeholder.markdown(f"🤖 {bot_reply}")

    st.session_state.bot_thinking = False
    # Add bot response to current session

