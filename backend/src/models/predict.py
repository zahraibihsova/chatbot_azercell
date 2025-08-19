# dummy generator to simulate streaming
def main(user_input):
    for i in range(3):
        yield f"🤔 Thinking... chunk {i+1} for: {user_input}\n"
