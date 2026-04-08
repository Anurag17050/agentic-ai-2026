# Agentic AI Lab — Assignments 1–4

A progressive series of AI agent implementations, starting from simple rule-based logic and advancing to multi-step planning with LLMs.

---

## Repository Structure

```
agentic-ai-lab/
├── day1/          # Assignment 1: Rule-Based AI Agent
├── day2/          # Assignment 2: Tool-Using AI Agent
├── day3/          # Assignment 3: LLM-Based Agent
├── day4/          # Assignment 4: Multi-Step Planning Agent
└── README.md
```

---

## Assignment 1: Rule-Based AI Agent

### Objective
Implement a simple AI agent using rule-based logic (keyword matching).

### Approach

The agent follows a three-stage pipeline:

```
Input → Decision → Action
```

- **Input Handler** — takes user command
- **Decision Logic** — identifies intent using keywords
- **Action Execution** — performs the corresponding action

### Features
- Greeting detection (`hello`, `hi`, `hey`)
- Date and time retrieval
- Combined date & time query
- Calculator (handles expressions extracted from natural language)
- Exit commands (`quit`, `bye`, `leave`)
- Multi-intent handling (one input → multiple actions)

### Key Concepts
- Rule-based reasoning
- Keyword matching
- Pattern extraction using regex
- Multi-intent detection

### Example Inputs
```
hi
can you tell me date and time
calculate 5+3
I want result of 6*2-1
```

### Tools Used
- Python 3
- `datetime` module
- `re` (regular expressions)

### How to Run
```bash
python3 day1/agent.py
```

---

## Assignment 2: Tool-Using AI Agent

### Objective
Extend the rule-based agent by introducing modular tool usage. Instead of performing actions directly, the agent identifies intent and delegates to the appropriate tool (function).

### Approach

```
User Input → Decision Logic → Tool Selection → Tool Execution → Output
```

### Features
- Natural language input handling
- Multiple intents supported in a single query
- Modular design with separate `agent.py` and `tools.py`
- Robust input processing (punctuation removal, normalization)

### Tools Implemented

| Tool | Description |
|---|---|
| Calculator | Extracts and evaluates math expressions; supports `+ - * / ( )` |
| Date & Time | Returns current system date and/or time |
| Weather (Mocked) | Returns predefined weather data for detected city names |
| Text Summarizer | Frequency-based sentence scoring; extracts key sentences |
| Word Count | Counts total words in the input |
| Palindrome Checker | Checks whether a word or number is a palindrome |

### Project Structure
```
day2/
├── agent.py      # Main agent logic (input, decision, execution)
├── tools.py      # All tool implementations
└── README.md
```

### Sample Inputs
```
hi calculate 5+3
what is the time
weather in delhi
summarize judiciary is an important pillar of democracy which ensures justice
check whether racecar is palindrome
count words in this sentence
```

### How to Run
```bash
cd day2
python3 agent.py
```

### Limitations
- Rule-based decision logic (no LLM)
- Weather tool is mocked (static data)
- Summarizer works best with longer inputs

---

## Assignment 3: LLM-Based Agent

### Objective
Replace rule-based decision logic with a Large Language Model. The LLM reads user input and decides which tool to call — no keyword matching, no if/else chains.

### Tech Stack

| Component | Tool |
|---|---|
| LLM Provider | Groq (free tier) |
| Model | `llama-3.3-70b-versatile` |
| Framework | LangChain + langchain-groq |
| Language | Python 3.12 |

### How It Works

```
User Input
    │
    ▼
LLM (Groq — llama-3.3-70b-versatile)
    │  Returns structured JSON:
    │  {"tools": [{"tool": "calculator", "input": "3+4"}]}
    │
    ▼
Tool Executor
    │
    ▼
Output printed + logged to logs.json
```

### Key Difference from Assignment 2

| Feature | Assignment 2 | Assignment 3 |
|---|---|---|
| Tool selection | Keyword matching | LLM decides |
| Multi-tool support | Limited | Full support |
| Summarizer | Extractive (sentence picking) | LLM rewrites in own words |
| Logs | None | Auto-saved to `logs.json` |

### Available Tools

| Tool | Example Trigger |
|---|---|
| `calculator` | "calculate 3+4", "what is 10*5" |
| `datetime` | "what is the time?", "today's date" |
| `weather` | "how is the weather in Mumbai?" |
| `summarizer` | "summarize the French Revolution" |
| `word_count` | "count words in this sentence" |
| `palindrome` | "is madam a palindrome?" |
| `greet` | "hello", "hi", "hey" |
| `exit` | "bye", "quit", "exit" |

### Multi-Tool Example
```
You: hi! can you solve 3+4/5-(2*4)?
[Tool selected: greet]    → Hello! How can I help you?
[Tool selected: calculator] → -4.2
```

### Project Structure
```
day3/
├── agent.py      # Main agent loop, LLM-based tool selector
├── tools.py      # Tool functions
├── logs.json     # Auto-generated interaction log
└── README.md
```

### Setup
```bash
pip install langchain langchain-groq langchain-core
```

Add your Groq API key in `agent.py` and `tools.py`:
```python
api_key="your-groq-api-key-here"
```
Get a free key at: https://console.groq.com

### How to Run
```bash
cd day3
python3 agent.py
```

### Sample Output
```
You: hello! what is 25 * 4?
[Tool selected: greet]
Agent: Hello! How can I help you?
[Tool selected: calculator]
Agent: 100

You: is racecar a palindrome?
[Tool selected: palindrome]
Agent: racecar is Palindrome
```

### Logs
Every interaction is saved to `logs.json`:
```json
[
  {
    "input": "what is 25 * 4?",
    "tool": "calculator",
    "output": "100"
  }
]
```

### Key Concepts Learned
- LLM-based decision making
- Prompt engineering for structured JSON output
- Tool abstraction and modular design
- Multi-tool call handling
- Persistent interaction logging

---

## Assignment 4: Multi-Step Planning Agent

### Objective
Build an agent that decomposes complex queries into sequential steps and executes them one at a time, passing context forward through each step.

### Approach

The agent uses two distinct LLM-powered roles:

**Planner** — receives the user query and breaks it into a JSON list of action-oriented steps:
```json
{"steps": ["step 1", "step 2", "step 3"]}
```

**Executor** — receives each step one at a time, with full context (original query + all prior results), and executes only the current step.

```
User Query
    │
    ▼
Planner LLM → ["step 1", "step 2", ...]
    │
    ▼
Executor LLM (runs step 1, then step 2, chaining results...)
    │
    ▼
Final Answer
```

### Example Interaction

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

### Project Structure
```
day4/
├── agent.py      # Planner + Executor logic
└── README.md
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| Two-prompt architecture | Keeps Planner and Executor focused and debuggable independently |
| Regex JSON extraction | Handles LLM responses that include surrounding text |
| Context chaining | Each executor call receives full prior history |
| No hardcoded tools | Pure LLM reasoning — no predefined functions |

### Key Concepts Learned
- Task decomposition with a Planner LLM
- Sequential reasoning with context chaining
- Intermediate output display
- Modular `plan()` and `execute_step()` design

### How to Run
```bash
pip install langchain-groq langchain-core
cd day4
python3 agent.py
```

---

## Progression Summary

| Assignment | Decision Logic | Tools | Multi-Step | Logs |
|---|---|---|---|---|
| 1 — Rule-Based | Keyword matching | Built-in actions | No | No |
| 2 — Tool-Using | Keyword matching | Modular tools.py | No | No |
| 3 — LLM-Based | LLM (Groq) | Modular tools.py | Via multi-tool | Yes |
| 4 — Planning | LLM (Groq) | Pure LLM reasoning | Yes (Planner) | No |

---

## Requirements

- Python 3.9+
- pip
- LangChain (`pip install langchain langchain-groq langchain-core`)
- Groq API key (free at https://console.groq.com)
