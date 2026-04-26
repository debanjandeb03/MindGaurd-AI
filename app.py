from flask import Flask, render_template, request
from llm.prompt import build_prompt
from llm.mistral_api import ask_mistral

app = Flask(__name__)

# 🔹 Format LLM Output
def format_output(text):
    category = ""
    reason = ""
    suggestions = []

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if line.lower().startswith("category"):
            category = line.split(":", 1)[-1].strip()

        elif line.lower().startswith("reason"):
            reason = line.split(":", 1)[-1].strip()

        elif line.startswith("-"):
            suggestions.append(line[1:].strip())

    # 🔹 Fallbacks (very important)
    if not category:
        category = "Unknown"

    if not reason:
        reason = text

    if not suggestions:
        suggestions = ["Take care of yourself and consider talking to someone you trust"]

    return category, reason, suggestions


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form["text"]

    # 🚨 Safety Check
    if any(word in user_input.lower() for word in ["suicide", "kill myself", "end my life", "die"]):
        return render_template(
            "result.html",
            category="⚠️ Critical",
            reason="User shows signs of self-harm risk.",
            suggestions=[
                "Please contact a trusted person immediately",
                "Reach out to a mental health helpline",
                "Seek professional help urgently"
            ]
        )

    prompt = build_prompt(user_input)
    response = ask_mistral(prompt)

    category, reason, suggestions = format_output(response)

    return render_template(
        "result.html",
        category=category,
        reason=reason,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)