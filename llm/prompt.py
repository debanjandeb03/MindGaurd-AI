def build_prompt(user_input):
    return f"""
You are a mental health assistant.

Carefully analyze the user's message.

Classify it into one of:
- Normal
- Stress
- Anxiety
- Depression

Respond STRICTLY in this format:

Category: <one word>

Reason:
<short explanation>

Suggestions:
- point 1
- point 2
- point 3

User message: "{user_input}"
"""