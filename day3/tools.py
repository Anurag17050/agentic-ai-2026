import os
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import re

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# Calculator
def calculator_tool(text):
    try:
        exp = "".join(re.findall(r"[0-9+\-*/().]", text))
        if exp == "":
            return "No valid expression found"
        return str(eval(exp))
    except:
        return "Invalid expression"

# Date & Time
def datetime_tool(query="both"):
    now = datetime.now()
    query = query.lower()
    if "time" in query and "date" not in query:
        return f"Time: {now.strftime('%H:%M:%S')}"
    elif "date" in query and "time" not in query:
        return f"Date: {now.date()}"
    else:
        return f"Date: {now.date()} | Time: {now.strftime('%H:%M:%S')}"

# Weather — LLM based
def weather_tool(text):
    try:
        if not text.strip():
            return "No weather query provided"
        response = llm.invoke([
            HumanMessage(content=f"Give a short 1-2 sentence mock weather response for this query: {text}")
        ])
        return response.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Summarizer — LLM based
def summarizer_tool(text):
    try:
        if not text.strip():
            return "No content to summarize"
        response = llm.invoke([
            HumanMessage(content=f"Summarize this in 2-3 sentences in your own words:\n\n{text}")
        ])
        return response.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Word Count
def word_count_tool(text):
    return f"Word count: {len(text.split())}"

# Palindrome
def palindrome_tool(text):
    words = re.findall(r'\b\w+\b', text.lower())
    ignore = {"check", "whether", "is", "palindrome", "or", "not"}
    words = [w for w in words if w not in ignore]
    if not words:
        return "No valid input"
    target = words[0]
    return f"{target} is Palindrome" if target == target[::-1] else f"{target} is Not Palindrome"
