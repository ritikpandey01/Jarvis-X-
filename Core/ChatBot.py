import time
from groq import Groq
from json import load, dump
import datetime
from dotenv import load_dotenv
import os
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

# System prompt for chatbot
SYSTEM_PROMPT = f"""
Hello, I am {USERNAME}, and you are {ASSISTANT_NAME}, an advanced AI chatbot with real-time information. Answer my queries concisely in English, even if the query is in another language. Do not provide time/date unless asked, and avoid excessive details or notes. Just answer the question and call me Sir.
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

def get_real_time_info() -> str:
    """Provides real-time date and time information."""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    return f"""
    Current date and time (use only if relevant):
    Day: {day}
    Date: {date}
    Month: {month}
    Year: {year}
    Time: {hour}:{minute}:{second}
    """

def clean_response(response: str) -> str:
    """Cleans the response by removing empty lines and extra whitespace."""
    lines = response.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

def is_valid_query(query: str) -> bool:
    """Validates if the query is suitable for processing."""
    return not re.match(r".*[\\/].*\.exe|.*[\\/].*\.py|&.*", query)

def answer_query(query: str, max_retries: int = 3) -> str:
    """Sends the user's query to the Groq API and returns the response."""
    # Sanitize and validate input
    query = query.strip()
    if not query:
        return "Please enter a valid query."
    
    if not is_valid_query(query):
        return "Invalid query. Please avoid command-line inputs."

    # Update chat history
    chat_history.append({"role": "user", "content": query})

    for attempt in range(max_retries):
        try:
            # Call Groq API
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "system", "content": get_real_time_info()},
                    *chat_history
                ],
                max_tokens=1024,
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
                return "No response received. Please try again."

            # Update chat history
            chat_history.append({"role": "assistant", "content": response_text})
            if len(chat_history) > 10:
                chat_history[:] = chat_history[-10:]
            with open(CHAT_LOG_PATH, "w") as f:
                dump(chat_history, f, indent=4)

            return clean_response(response_text)

        
        except Exception:
            return "An unexpected error occurred. Please try again."

if __name__ == "__main__":
    while True:
        user_input = input().strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        print(answer_query(user_input))
