# Assignment 1: Rule-Based AI Agent

## Objective
To implement a simple AI agent using rule-based logic (keyword matching).

## Approach
The agent follows a pipeline:

Input → Decision → Action

- Input Handler: Takes user command
- Decision Logic: Identifies intent using keywords
- Action Execution: Performs corresponding action

## Features
- Greeting (hello, hi, hey)
- Date and Time retrieval
- Combined Date & Time
- Calculator (handles expressions from sentences)
- Exit commands (quit, bye, leave)
- Multi-intent handling (one input → multiple actions)

## Key Concepts
- Rule-based reasoning
- Keyword matching
- Pattern extraction using regex
- Multi-intent detection

## Example Inputs
- hi
- can you tell me date and time
- calculate 5+3
- I want result of 6*2-1

## Output
Agent responds based on detected intent(s).

## Tools Used
- Python 3
- datetime module
- re (regular expressions)

## How to Run
```bash
python3 agent.py
