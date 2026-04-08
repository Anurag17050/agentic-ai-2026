import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json
import re

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# ── Step 1: Planner — breaks query into steps ───────────────
PLANNER_PROMPT = """
You are a planning agent. Break the user query into clear sequential steps.
Return ONLY a JSON like:
{"steps": ["step 1 description", "step 2 description", "step 3 description"]}

Keep steps short and action-oriented.
Return ONLY the JSON. No explanation.
"""

def plan(user_input):
    response = llm.invoke([
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=user_input)
    ])
    raw = response.content.strip()
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        return json.loads(match.group()).get("steps", [])
    return []

# ── Step 2: Executor — executes each step with context ──────
EXECUTOR_PROMPT = """
You are a step executor. You will be given:
- The original user query
- All steps planned
- Steps completed so far with their results
- The current step to execute

Execute ONLY the current step using the context from previous steps.
Return a short, clear result for this step only.
"""

def execute_step(user_input, all_steps, completed_steps, current_step):
    context = f"""
Original query: {user_input}

All planned steps:
{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(all_steps))}

Completed steps:
{chr(10).join(f"- {s['step']}: {s['result']}" for s in completed_steps) if completed_steps else "None yet"}

Current step to execute: {current_step}
"""
    response = llm.invoke([
        SystemMessage(content=EXECUTOR_PROMPT),
        HumanMessage(content=context)
    ])
    return response.content.strip()

# ── Main loop ───────────────────────────────────────────────
print("Assignment 4: Multi-Step Planning Agent")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break

    print("\n Planner is breaking down your query...\n")
    steps = plan(user_input)

    if not steps:
        print("Could not plan steps. Try rephrasing.\n")
        continue

    print(f" {len(steps)} steps planned:\n")
    for i, step in enumerate(steps):
        print(f"  {i+1}. {step}")
    print()

    completed = []

    for i, step in enumerate(steps):
        print(f"--- Step {i+1}: {step} ---")
        result = execute_step(user_input, steps, completed, step)
        print(f"Result: {result}\n")
        completed.append({"step": step, "result": result})

    print("=== Final Answer ===")
    print(completed[-1]["result"])
    print()
