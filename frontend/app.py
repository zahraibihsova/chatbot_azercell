import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/bedrock-chat"

st.set_page_config(page_title="Betty Chatbot💅🏻", layout="wide")

# Background and styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #9ECAD6;  
    color: #FFEAEA;               
}
[data-testid="stSidebar"] > div:first-child {
    background: #748DAE; 
    border-radius: 10px;
    padding: 10px;
}
.chat-box {
    background: rgba(255, 255, 255, 0.7);
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: black;
    display: flex;
    align-items: flex-start;
}
.icon {
    font-size: 22px;
    margin-right: 10px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Betty Chat 💅🏻")
    st.markdown(
        """
        ### About Betty the bot 🤖  
        Betty is an AI-powered chatbot built with Streamlit and FastAPI.  
        - Can answer your questions  
        - Optionally uses **Azercell Knowledge Base** for more specific answers  
        - Is happy to help you anytime  
        """
    )
    # Option to choose KB mode for chat
    use_kb = st.checkbox("Use Azercell Knowledge Base", value=False)
    # Reset session
    if st.button("New Chat"):
        st.session_state.clear()
        st.rerun()

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Talk to Betty 👱🏻‍♀️")

# Input
user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip() != "":
    st.session_state.history.append({"user": user_input, "betty": "..."})
    try:
        # if user asks name, Betty answers directly
        if "your name" in user_input.lower() or "who are you" in user_input.lower():
            betty_response = "My name is Betty 💅🏻, nice to meet you!"
        else:
            # sending use_kb parameter to backend
            response = requests.get(
                BACKEND_URL,
                params={"query": user_input, "use_kb": str(use_kb).lower()},
            )
            if response.status_code == 200:
                betty_response = response.text
            else:
                betty_response = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        betty_response = f"Error connecting to backend: {str(e)}"

    st.session_state.history[-1]["betty"] = betty_response

# icons visible after you write message
for chat in st.session_state.history:
    st.markdown(
        f"<div class='chat-box'><span class='icon'>👱🏻‍♀️</span><b>You:</b> {chat['user']}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='chat-box'><span class='icon'>🤖</span><b>Betty:</b> {chat['betty']}</div>",
        unsafe_allow_html=True,
    )

# Clear part to clear chat history
if st.button("Clear Chat"):
    st.session_state.clear()
    st.rerun()
