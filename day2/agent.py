from tools import (
    calculator_tool,
    datetime_tool,
    weather_tool,
    summarizer_tool,
    word_count_tool,
    palindrome_tool,
)
import re

# ── Input Handler ────────────────────────────────────────────
def get_input():
    return input("Enter command: ").strip()

# ── Normalize: lowercase + strip punctuation for keyword matching ──
def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower())

# ── Decision Logic ───────────────────────────────────────────
def decide(user_input):
    n = normalize(user_input)
    words = n.split()
    actions = []

    # greet — match on cleaned words so "hello!" works
    if any(w in ["hello", "hi", "hey"] for w in words):
        actions.append("greet")

    # calculator — math operators OR explicit keywords
    if any(w in ["calculate", "result", "evaluate", "expression"] for w in words) or \
       any(op in user_input for op in ["+", "-", "*", "/"]):
        actions.append("calc")

    # date / time
    if "date" in words and "time" in words:
        actions.append("datetime")
    elif "date" in words:
        actions.append("date")
    elif "time" in words:
        actions.append("time")

    # weather
    if "weather" in words:
        actions.append("weather")

    # summarize
    if any(w in words for w in ["summarize", "summary"]):
        actions.append("summary")

    # word count
    if "count" in words:
        actions.append("count")

    # palindrome
    if "palindrome" in words:
        actions.append("palindrome")

    # exit
    if any(w in words for w in ["exit", "quit", "bye", "leave"]):
        actions.append("exit")

    if not actions:
        actions.append("unknown")

    return actions

# ── Action Execution ─────────────────────────────────────────
def act(actions, user_input):
    for action in actions:
        if action == "greet":
            print("Hello! How can I help you?")

        elif action == "calc":
            print("Result:", calculator_tool(user_input))

        elif action == "date":
            from datetime import datetime
            print("Date:", datetime.now().date())

        elif action == "time":
            from datetime import datetime
            print("Time:", datetime.now().time())

        elif action == "datetime":
            print(datetime_tool())

        elif action == "weather":
            print(weather_tool(user_input))

        elif action == "summary":
            result = summarizer_tool(user_input)
            print("Summary:", result)

        elif action == "count":
            print(word_count_tool(user_input))

        elif action == "palindrome":
            print(palindrome_tool(user_input))

        elif action == "exit":
            print("Goodbye!")
            exit()

        else:
            print("Sorry, I don't understand that command.")

# ── Main Loop ────────────────────────────────────────────────
print("Assignment 2: Tool-Using Agent  |  type 'exit' to quit\n")
while True:
    ui = get_input()
    if not ui:
        continue
    actions = decide(ui)
    act(actions, ui)
