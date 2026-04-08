import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from tools import (
    calculator_tool, datetime_tool, weather_tool,
    summarizer_tool, word_count_tool, palindrome_tool
)
import json
import os
import re

# ── LLM setup ──────────────────────────────────────────────
llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# ── Logger ──────────────────────────────────────────────────
LOG_FILE = "logs.json"

def log(user_input, tool_selected, output):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append({
        "input": user_input,
        "tool": tool_selected,
        "output": output
    })
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# ── System prompt ───────────────────────────────────────────
SYSTEM_PROMPT = """
You are a tool selector. Based on user input, return ONLY a JSON like:
{"tools": [{"tool": "<tool_name>", "input": "<cleaned input>"}, ...]}

Available tools:
- calculator   → math expressions (e.g. 2+3, 10*5)
- datetime     → current date or time (input: "date", "time", or "both")
- weather      → weather queries
- summarizer   → summarize any text
- word_count   → count words in text
- palindrome   → check if a word is palindrome
- greet        → hello, hi, hey
- exit         → quit, bye, exit
- unknown      → anything else

If user does multiple things in one message, return multiple tools in the list.
Return ONLY the JSON. No explanation.
"""

# ── LLM decides tools ───────────────────────────────────────
def decide(user_input):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input)
    ]
    response = llm.invoke(messages)
    raw = response.content.strip()

    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        parsed = json.loads(match.group())
        return parsed.get("tools", [{"tool": "unknown", "input": user_input}])
    return [{"tool": "unknown", "input": user_input}]

# ── Execute tool ────────────────────────────────────────────
def act(tool, cleaned_input):
    if tool == "calculator":
        return calculator_tool(cleaned_input)
    elif tool == "datetime":
        return datetime_tool(cleaned_input)
    elif tool == "weather":
        return weather_tool(cleaned_input)
    elif tool == "summarizer":
        return summarizer_tool(cleaned_input)
    elif tool == "word_count":
        return word_count_tool(cleaned_input)
    elif tool == "palindrome":
        return palindrome_tool(cleaned_input)
    elif tool == "greet":
        return "Hello! Anurag"
    elif tool == "exit":
        print("Goodbye!")
        exit()
    else:
        return "Sorry, I don't understand that."

# ── Main loop ───────────────────────────────────────────────
print("Assignment 3: LLM-Based Agent (Groq + LangChain)")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue

    decisions = decide(user_input)

    for decision in decisions:
        tool    = decision.get("tool", "unknown")
        cleaned = decision.get("input", user_input)

        print(f"[Tool selected: {tool}]")
        output = act(tool, cleaned)
        print(f"Agent: {output}")
        log(user_input, tool, output)

    print()
