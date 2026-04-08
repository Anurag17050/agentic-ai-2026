# Assignment 4: Multi-Step Planning Agent

## Overview

This assignment implements a **Multi-Step Planning Agent** using LangChain and the Groq-hosted LLaMA 3.3 70B model. The agent takes a user query, breaks it into a sequence of logical steps using a Planner, and executes each step one by one using an Executor — passing context from previous steps forward.

---

## Approach

The agent is split into two distinct LLM-powered roles:

### 1. Planner
- Receives the raw user query
- Uses the LLM to decompose it into short, action-oriented steps
- Returns a structured JSON list of steps: `{"steps": ["step 1", "step 2", ...]}`

### 2. Executor
- Receives each step one at a time
- Has full context: the original query, all planned steps, and results from completed steps
- Executes only the current step, building on prior results

This separation ensures clean **task decomposition** and **sequential reasoning** — the core goals of Assignment 4.

---

## File Structure

```
day4/
├── agent.py       # Main agent loop with Planner and Executor
└── README.md      # This file
```

---

## How to Run

### Prerequisites

```bash
pip install langchain-groq langchain-core
```

You also need a [Groq API key](https://console.groq.com/) set in `agent.py`.

### Run the agent

```bash
python3 agent.py
```

---

## Example Interaction

**Query:** `find the average of 5, 10, 15 and summarize the result`

```
 4 steps planned:
  1. Add the numbers 5, 10, 15
  2. Count the total numbers
  3. Divide the sum by the count
  4. Summarize the result

--- Step 1: Add the numbers 5, 10, 15 ---
Result: 5 + 10 + 15 = 30

--- Step 2: Count the total numbers ---
Result: There are 3 numbers.

--- Step 3: Divide the sum by the count ---
Result: 30 / 3 = 10

--- Step 4: Summarize the result ---
Result: The average of 5, 10, 15 is 10.

=== Final Answer ===
The average of 5, 10, 15 is 10.
```

---

## Key Concepts Demonstrated

| Concept | How it's implemented |
|---|---|
| Task decomposition | Planner LLM breaks query into JSON steps |
| Sequential reasoning | Executor receives all prior results as context |
| Intermediate outputs | Each step result is printed before moving to the next |
| Modular design | `plan()` and `execute_step()` are separate functions |
| LLM integration | LangChain + Groq (LLaMA 3.3 70B) |

---

## Design Decisions

- **Two-prompt architecture:** Keeping the Planner and Executor as separate system prompts makes each role focused and easier to debug.
- **Regex JSON extraction:** The planner uses `re.search` to extract the JSON block even if the LLM adds surrounding text, making it more resilient.
- **Context chaining:** Each executor call receives the full history of completed steps, enabling the model to reference earlier results naturally (e.g., using the sum from Step 1 when dividing in Step 3).
- **No hardcoded tools:** Unlike Assignments 1–3, this agent relies entirely on LLM reasoning rather than predefined functions, demonstrating pure planning-based execution.
