import time
from groq import Groq
from json import load, dump
from dotenv import load_dotenv
import os
from typing import List
import re

# Load environment variables
load_dotenv()
USERNAME = os.getenv("Username", "User")
ASSISTANT_NAME = os.getenv("Assistantname", "Jarvo")
GROQ_API_KEY = os.getenv("GroqAPIKey")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Supported task categories
TASK_CATEGORIES = [
    "exit",
    "general",
    "realtime",
    "open",
    "close",
    "play",
    "generate_image",
    "system",
    "content",
    "google_search",
    "youtube_search",
    "reminder",
]

# System prompt for query classification
SYSTEM_PROMPT = f"""
You are {ASSISTANT_NAME}, a Decision-Making Assistant for {USERNAME} that classifies user queries into task categories. Do not answer the query; only classify it. Return classifications in the format 'category (details)' or 'category' for 'exit', with multiple tasks separated by commas. Valid categories: exit, general, realtime, open, close, play, generate_image, system, content, google_search, youtube_search, reminder.

Rules:
- 'general (query)': For queries answerable without real-time data (e.g., 'who was akbar?', 'how to study?', 'what is python?', 'thanks!', 'what time is it?', 'who is he?').
- 'realtime (query)': For queries needing up-to-date information (e.g., 'who is indian prime minister?', 'today's news', 'facebook's recent update').
- 'open (app/website)': For opening apps/websites (e.g., 'open chrome', 'open facebook').
- 'close (app/website)': For closing apps/websites (e.g., 'close notepad').
- 'play (song)': For playing songs (e.g., 'play let her go').
- 'generate_image (prompt)': For image generation (e.g., 'generate image of a lion').
- 'reminder (datetime message)': For reminders (e.g., 'reminder 9:00pm 25th june meeting').
- 'system (task)': For system tasks (e.g., 'mute', 'volume up').
- 'content (topic)': For writing content (e.g., 'write python script').
- 'google_search (topic)': For Google searches (e.g., 'search python tutorials').
- 'youtube_search (topic)': For YouTube searches (e.g., 'search cooking videos').
- 'exit': For ending conversation (e.g., 'bye', 'quit').
- For multiple tasks, return each separated by commas (e.g., 'open chrome, open firefox').
- For empty or unsupported queries, return 'general (query)'.

Examples:
- 'who was akbar?' → 'general who was akbar?'
- 'open chrome, open firefox' → 'open chrome, open firefox'
- 'reminder 9:00pm meeting' → 'reminder 9:00pm meeting'
- 'bye' → 'exit'
- '' → 'general empty query'
"""

# Initialize chat history
CHAT_LOG_PATH = "Data/ChatLog.json"
chat_history = []

try:
    with open(CHAT_LOG_PATH, "r") as f:
        chat_history = load(f)
except FileNotFoundError:
    os.makedirs("Data", exist_ok=True)
    with open(CHAT_LOG_PATH, "w") as f:
        dump([], f)

def is_valid_query(query: str) -> bool:
    """Validates if the query is suitable for processing."""
    return not re.match(r".*[\\/].*\.exe|.*[\\/].*\.py|&.*", query)

def classify_user_query(query: str, max_retries: int = 3) -> List[str]:
    """Classifies a user query into task categories using Groq's API."""
    # Sanitize and validate input
    query = query.strip()
    if not query:
        return ["general empty query"]
    
    if not is_valid_query(query):
        return ["general invalid query"]

    # Update chat history
    chat_history.append({"role": "user", "content": query})

    for attempt in range(max_retries):
        try:
            # Call Groq API
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *chat_history
                ],
                max_tokens=256,
                temperature=0.7,
                stream=True
            )

            # Process stream
            response_text = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content

            response_text = response_text.replace("</s>", "").strip()
            if not response_text:
                return ["general empty response"]

            # Clean and split response
            response_text = re.sub(r"\s+", " ", response_text)
            tasks = [task.strip() for task in response_text.split(",") if task.strip()]

            # Validate tasks
            valid_tasks = []
            for task in tasks:
                if any(task.startswith(category) for category in TASK_CATEGORIES):
                    valid_tasks.append(task)
                else:
                    valid_tasks.append(f"general {query}")

            # Update chat history
            chat_history.append({"role": "assistant", "content": ", ".join(valid_tasks)})
            if len(chat_history) > 10:
                chat_history[:] = chat_history[-10:]
            with open(CHAT_LOG_PATH, "w") as f:
                dump(chat_history, f, indent=4)

            return valid_tasks

        
        except Exception:
            return ["general unexpected error"]

if __name__ == "__main__":
    while True:
        user_input = input().strip().lower()
        if user_input in ["exit", "quit"]:
            break
        print(classify_user_query(user_input))
