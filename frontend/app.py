import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/bedrock-chat"
#if using docker
#BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/bedrock-chat") 

st.set_page_config(page_title="Betty Chatbot💅🏻", layout="wide") #name of the page

# backgorund (only color) and color of texts
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #9CAFAA;  
    color: black;               
}
[data-testid="stSidebar"] > div:first-child {
    background: #D6DAC8; 
    border-radius: 10px;
    padding: 10px;
}
.chat-box {
    background: rgba(255, 255, 255, 0.7);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: black;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar for starting a new chat
with st.sidebar:
    st.title("Betty Chat")
    if st.button("New Chat"):
        st.session_state.clear()
        st.rerun()

# chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Talk to Betty 👱🏻‍♀️")

# Input box 
user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip() != "":
    st.session_state.history.append({"user": user_input, "betty": "..."})
    try:
        response = requests.get(BACKEND_URL, params={"query": user_input})
        if response.status_code == 200:
            betty_response = response.text
        else:
            betty_response = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        betty_response = f"Error connecting to backend: {str(e)}"
    
    st.session_state.history[-1]["betty"] = betty_response

# Chat history (doesn't work fully will be fixed later)
for chat in st.session_state.history:
    st.markdown(f"<div class='chat-box'><b>You:</b> {chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-box'><b>Betty:</b> {chat['betty']}</div>", unsafe_allow_html=True)

# Clear button
if st.button("Clear Chat"):
    st.session_state.clear()
    st.rerun()
