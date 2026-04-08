from datetime import datetime
from collections import Counter   # was MISSING — caused every summarize to silently crash
import re

# ── Calculator ───────────────────────────────────────────────
def calculator_tool(text):
    """Extract and evaluate a math expression from natural language."""
    try:
        exp = "".join(re.findall(r"[0-9+\-*/().\s]", text)).strip()
        # Remove stray spaces inside the expression
        exp = re.sub(r"\s+", "", exp)
        if not exp:
            return "No valid expression found"
        return str(eval(exp))
    except Exception:
        return "Invalid expression"

# ── Date & Time ──────────────────────────────────────────────
def datetime_tool():
    now = datetime.now()
    return f"Date: {now.date()}  |  Time: {now.strftime('%H:%M:%S')}"

# ── Weather (mock) ───────────────────────────────────────────
CITY_WEATHER = {
    "mumbai":    ("Mumbai", "32°C, Humid"),
    "delhi":     ("Delhi",  "28°C, Sunny"),
    "bangalore": ("Bangalore", "24°C, Partly Cloudy"),
    "chennai":   ("Chennai",   "35°C, Hot"),
    "kolkata":   ("Kolkata",   "30°C, Cloudy"),
}

def weather_tool(text):
    text_lower = text.lower()
    for key, (city, condition) in CITY_WEATHER.items():
        if key in text_lower:
            return f"Weather in {city}: {condition} (mock)"
    return "Weather: 30°C, Clear skies (mock — no city detected)"

# ── Summarizer ───────────────────────────────────────────────
# Command prefixes to strip before processing
_COMMAND_RE = re.compile(
    r"^\s*(give\s+me\s+a\s+summary\s+(of|on)|summarize|summary\s+of|summary)\s*",
    re.IGNORECASE,
)

STOP_WORDS = {
    "the","a","an","is","it","in","on","of","and","or","to","that","this",
    "was","are","with","for","as","at","be","by","its","he","she","they",
    "we","you","i","has","have","had","but","not","from","also","which",
    "who","what","when","where","how","very","just","so","do","did",
}

def summarizer_tool(text):
    # Strip the command verb so only the content remains
    content = _COMMAND_RE.sub("", text).strip()

    if len(content.split()) < 5:
        return (
            f'"{content}" is too short to summarize. '
            "Please provide a full paragraph or multiple sentences."
        )

    sentences = re.split(r"(?<=[.!?])\s+", content.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

    if not sentences:
        return "No meaningful content found to summarize."

    if len(sentences) <= 2:
        return " ".join(sentences)

    # Score sentences by content-word frequency
    all_words = re.findall(r"\b\w+\b", content.lower())
    freq = Counter(w for w in all_words if w not in STOP_WORDS)

    def score(sentence):
        words = [w for w in re.findall(r"\b\w+\b", sentence.lower()) if w not in STOP_WORDS]
        return sum(freq[w] for w in words) / len(words) if words else 0

    scored = sorted(enumerate(sentences), key=lambda x: score(x[1]), reverse=True)
    top_indices = sorted(i for i, _ in scored[:2])
    return " ".join(sentences[i] for i in top_indices)

# ── Word Count ───────────────────────────────────────────────
def word_count_tool(text):
    count = len(text.split())
    return f"Word count: {count}"

# ── Palindrome ───────────────────────────────────────────────
_PALINDROME_NOISE = {
    "check", "whether", "is", "a", "are", "palindrome", "or", "not",
    "can", "you", "tell", "me", "if", "the", "word", "number", "u",
    "please", "hey", "hi",
}

def palindrome_tool(text):
    """
    Extracts the actual target (word or number) from queries like:
      'is 1221 a palindrome'
      'check whether racecar is palindrome or not'
      'can u check whether 1329087468 is palindrome or not'
    Strategy: prefer any numeric token; otherwise take the longest
    non-noise word — that's almost always the intended subject.
    """
    tokens = re.findall(r"\b[\w]+\b", text.lower())

    # Prefer a numeric token — numbers are unambiguous
    numbers = [t for t in tokens if t.isdigit()]
    if numbers:
        target = numbers[0]
    else:
        # Take the longest word not in the noise set
        candidates = [t for t in tokens if t not in _PALINDROME_NOISE]
        if not candidates:
            return "No valid word or number found to check."
        target = max(candidates, key=len)

    result = "a Palindrome ✓" if target == target[::-1] else "NOT a Palindrome ✗"
    return f'"{target}" is {result}'
