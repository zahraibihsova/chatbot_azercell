import streamlit as st
import requests

st.set_page_config(
    page_title="Chatbot Interface",
    layout="centered",
    page_icon="💅🏼",
)

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <h2>🤖 DataMinds'25 ML Predictor</h2>
        <p>Chat with the model live.</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    if st.button("🆕 New Chat"):
        st.session_state["messages"] = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("💬 Chatbot")

# User input
user_input = st.text_input("Type your message:", key="input")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.session_state["messages"].append({"role": "bot", "content": "🤔 Thinking..."})

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")

# Send message to backend if last bot message is "Thinking..."
if st.session_state["messages"] and st.session_state["messages"][-1]["content"] == "🤔 Thinking...":
    last_user_msg = [m for m in st.session_state["messages"] if m["role"] == "user"][-1]["content"]
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": last_user_msg},
            stream=True,
        )
        bot_response = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                bot_response += chunk.decode()
                st.session_state["messages"][-1]["content"] = bot_response
                st.experimental_rerun()  # remove or replace in newer Streamlit
    except Exception as e:
        st.session_state["messages"][-1]["content"] = f"Error: {e}"
