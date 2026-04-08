# Assignment 2: Tool-Using AI Agent

## Objective

The objective of this assignment is to extend a rule-based AI agent by introducing **tool usage**.
Instead of directly performing actions, the agent identifies the user’s intent and calls the appropriate tool (function) to perform the task.

---

## Overview

This project implements a **modular AI agent** that follows a structured pipeline:

**User Input → Decision Logic → Tool Selection → Tool Execution → Output**

* The agent takes natural language input from the user.
* It processes and normalizes the input.
* Based on keywords and patterns, it decides which tool(s) to use.
* The selected tool is executed.
* The output is displayed to the user.

---

## Features

* Handles **natural language inputs**
* Supports **multiple intents in a single query**
* Modular design with separate **agent** and **tools**
* Robust input processing (punctuation removal, normalization)
* Multiple tools integrated into a single agent system

---

## Tools Implemented

### 1. Calculator Tool

* Extracts and evaluates mathematical expressions from text
* Supports operators: `+ - * / ( )`
* Example:

  * Input: `calculate 2+3*5`
  * Output: `Result: 17`

---

### 2. Date & Time Tool

* Provides current system date and/or time
* Example:

  * Input: `what is time`
  * Output: `Time: 14:32:10`

---

### 3. Weather Tool (Mocked)

* Returns predefined weather data
* Detects city names (Mumbai, Delhi, etc.)
* Example:

  * Input: `weather in mumbai`
  * Output: `Weather in Mumbai: 32°C, Humid (mock)`

> Note: This is a **mock implementation**, not real-time data.

---

### 4. Text Summarizer

* Extracts key information from multi-sentence input
* Uses frequency-based sentence scoring
* Removes stopwords and ranks sentences
* Example:

  * Input: paragraph text
  * Output: concise summary

> Note: Works best for longer text inputs.

---

### 5. Word Count Tool

* Counts total words in the input
* Example:

  * Input: `count words in this sentence`
  * Output: `Word count: 6`

---

### 6. Palindrome Checker

* Checks whether a word or number is a palindrome
* Extracts meaningful target from natural language input
* Example:

  * Input: `check whether 1221 is palindrome`
  * Output: `"1221" is a Palindrome ✓`

---

## Project Structure

```
day2/
├── agent.py      # Main agent logic (input, decision, execution)
├── tools.py      # All tool implementations
└── README.md
```

---

## How to Run (WSL Ubuntu)

### Step 1: Navigate to project folder

```
cd ~/agentic-ai-lab/day2
```

### Step 2: (Optional) Activate virtual environment

```
source venv/bin/activate
```

### Step 3: Run the agent

```
python3 agent.py
```

---

## Sample Inputs

```
hi calculate 5+3
what is the time
tell me date and time
weather in delhi
summarize judiciary is an important pillar of democracy which ensures justice
check whether racecar is palindrome
count words in this sentence
```

---

## Expected Learning Outcomes

* Understanding **tool-based AI agent architecture**
* Separation of **decision logic and execution**
* Handling **natural language inputs**
* Designing **modular and reusable systems**
* Implementing **multi-step processing pipelines**

---

## Limitations

* Uses **rule-based decision logic** (no AI/LLM yet)
* Weather tool is **mocked (static data)**
* Summarizer performs best with **longer inputs**
* Limited understanding of complex natural language

---

## Conclusion

This assignment demonstrates how an AI agent can:

* Interpret user input
* Select appropriate tools
* Execute tasks in a modular way

It serves as the foundation for **Assignment 3**, where:

* Rule-based logic will be replaced with **LLM-based decision making**
* The agent will become more intelligent and flexible
