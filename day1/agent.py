from datetime import datetime
import re

# 1. Input Handler
def get_input():
    return input("Enter a query/command: ")

# 2. Decision Logic (MULTI-INTENT)
def decide(user_input):
    user_input = user_input.lower()
    actions = []

    # greet
    if any(w in user_input for w in ["hello", "hi", "hey"]):
        actions.append("greet")

    # calculation
    if any(w in user_input for w in ["calculate", "result", "evaluate", "expression", "+", "-", "*", "/"]):
        actions.append("calc")

    # date & time
    if "date" in user_input and "time" in user_input:
        actions.append("datetime")
    elif "date" in user_input:
        actions.append("date")
    elif "time" in user_input:
        actions.append("time")

    # exit
    if any(w in user_input for w in ["exit", "quit", "leave", "bye"]):
        actions.append("exit")

    # fallback
    if not actions:
        actions.append("unknown")

    return actions

# Extract only numbers & operators
def extract_expression(text):
    return "".join(re.findall(r"[0-9+\-*/().]", text))

# 3. Action Execution
def act(action, user_input):
    if action == "greet":
        print("Hello! Anurag")

    elif action == "date":
        print("Date:", datetime.now().date())

    elif action == "time":
        print("Time:", datetime.now().time())

    elif action == "datetime":
        now = datetime.now()
        print("Date:", now.date())
        print("Time:", now.time())

    elif action == "calc":
        try:
            exp = extract_expression(user_input)
            if exp == "":
                print("No valid expression found")
            else:
                print("Result:", eval(exp))
        except:
            print("Invalid expression")

    elif action == "exit":
        print("Exiting...")
        exit()

    else:
        print("Sorry, I don't understand.")

# Main Loop
while True:
    ui = get_input()
    actions = decide(ui)

    for action in actions:
        act(action, ui)
