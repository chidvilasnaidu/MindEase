MAX_TURNS = 4


def initialize_memory():
    return []


def update_memory(history, user_input, assistant_response):
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": assistant_response})

    # Keep only last N turns to reduce token usage
    if len(history) > MAX_TURNS * 2:
        history = history[-MAX_TURNS * 2:]

    return history


def build_conversation_context(history):
    context = ""
    for message in history:
        role = message["role"].capitalize()
        content = message["content"]
        context += f"{role}: {content}\n"
    return context