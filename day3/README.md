# Assignment 3: LLM-Based Agent

## Objective
Replace the rule-based decision logic from Assignment 2 with a Large Language Model (LLM). The LLM reads the user's input and decides which tool to call — no keyword matching, no if/else chains.

---

## Tech Stack

| Component | Tool Used |
|---|---|
| LLM Provider | [Groq](https://console.groq.com) (Free) |
| Model | `llama-3.3-70b-versatile` (Meta Llama 3.3) |
| Framework | LangChain + langchain-groq |
| Language | Python 3.12 |

---

## Folder Structure

```
day3/
├── agent.py       → Main agent loop, LLM-based tool selector
├── tools.py       → Tool functions (calculator, datetime, weather, summarizer, etc.)
├── logs.json      → Auto-generated log of all inputs, tools used, and outputs
└── README.md
```

---

## How It Works

```
User Input
    │
    ▼
LLM (Groq - llama-3.3-70b-versatile)
    │
    │  Reads the input and returns JSON:
    │  {"tools": [{"tool": "calculator", "input": "3+4"}]}
    │
    ▼
Tool Executor (act function)
    │
    ▼
Output printed + logged to logs.json
```

### Key difference from Assignment 2

| Feature | Assignment 2 | Assignment 3 |
|---|---|---|
| Tool selection | Keyword matching (`if "calculate" in text`) | LLM decides |
| Multi-tool | Not supported | Supported |
| Summarizer | Extractive (sentence picking) | LLM rewrites in own words |
| Weather | `if "cold"/"hot"` mock | LLM generates response |
| Logs | None | `logs.json` auto-saved |

---

## Available Tools

| Tool | Trigger Example |
|---|---|
| `calculator` | "calculate 3+4", "what is 10*5" |
| `datetime` | "what is the time?", "today's date" |
| `weather` | "how is the weather in Mumbai?" |
| `summarizer` | "summarize the French Revolution" |
| `word_count` | "count words in this sentence" |
| `palindrome` | "is madam a palindrome?" |
| `greet` | "hello", "hi", "hey" |
| `exit` | "bye", "quit", "exit" |

---

## Multi-Tool Support

If the user asks multiple things in one message, the LLM returns multiple tools and all are executed in order.

**Example:**
```
You: hi! can you solve 3+4/5-(2*4) and give the result
[Tool selected: greet]
Agent: Hello! How can I help you?
[Tool selected: calculator]
Agent: -4.2
```

---

## Setup & Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install langchain langchain-groq langchain-core
```

Add your Groq API key in both `agent.py` and `tools.py`:
```python
api_key="your-groq-api-key-here"
```

Get a free API key at: https://console.groq.com

---

## Running the Agent

```bash
python3 agent.py
```

---

## Sample Output

```
Assignment 3: LLM-Based Agent (Groq + LangChain)
Type 'exit' to quit

You: hello! what is 25 * 4?
[Tool selected: greet]
Agent: Hello! How can I help you?
[Tool selected: calculator]
Agent: 100

You: what is the time now?
[Tool selected: datetime]
Agent: Time: 21:05:51

You: today's date only
[Tool selected: datetime]
Agent: Date: 2026-04-07

You: summarize AI is transforming the world rapidly across all industries
[Tool selected: summarizer]
Agent: AI is revolutionizing industries at an unprecedented pace, reshaping how businesses operate and people work.

You: is racecar a palindrome?
[Tool selected: palindrome]
Agent: racecar is Palindrome

You: bye
[Tool selected: exit]
Agent: Goodbye!
```

---

## Logs

Every interaction is automatically saved to `logs.json`:

```json
[
  {
    "input": "what is 25 * 4?",
    "tool": "calculator",
    "output": "100"
  },
  {
    "input": "summarize AI is transforming the world",
    "tool": "summarizer",
    "output": "AI is revolutionizing industries at an unprecedented pace."
  }
]
```

---

## Key Concepts Learned

- **LLM-based decision making** — replacing if/else with a language model
- **Prompt engineering** — instructing the LLM to return structured JSON
- **Tool abstraction** — clean separation between decision and execution
- **Multi-tool calls** — handling multiple intents in a single user message
- **Logging** — maintaining a persistent record of agent actions
