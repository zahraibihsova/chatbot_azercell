import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/bedrock-chat"

st.set_page_config(page_title="Betty Chatbot👱🏻‍♀️", layout="wide")

# Sidebar for starting a new chat
with st.sidebar:
    st.title("Betty Chat")
    if st.button("New Chat"):
        st.session_state.clear()
        st.rerun()


# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Talk to Betty 💅🏻")

# Input box for user
user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip() != "":
    st.session_state.history.append({"user": user_input, "betty": "..."})
    # Send request to backend
    try:
        response = requests.get(BACKEND_URL, params={"query": user_input})
        if response.status_code == 200:
            betty_response = response.text
        else:
            betty_response = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        betty_response = f"Error connecting to backend: {str(e)}"
    
    # Update last entry with actual response
    st.session_state.history[-1]["betty"] = betty_response

# Display chat history
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Betty:** {chat['betty']}")
    st.markdown("---")

# Clear button at bottom
if st.button("Clear Chat"):
    st.session_state.clear()
    st.rerun()

