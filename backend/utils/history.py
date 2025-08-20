chat_history = {}

def add_to_history(user_id: str, user_message: str, bot_message: str):
    if user_id not in chat_history:
        chat_history[user_id] = []
    chat_history[user_id].append({"user": user_message, "bot": bot_message})

def get_history(user_id: str):
    return chat_history.get(user_id, [])
