import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import mtranslate as mt

# Load environment variables
config = dotenv_values(".env")
INPUT_LANGUAGE = config.get("InputLanguage", "en").lower()
TEMP_DIR = Path("Data")
DATA_DIR = Path("Data")
DATA_DIR.mkdir(exist_ok=True)

# HTML template with improved structure
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Speech Recognition</title>
    <script>
        let recognition;
        function startRecognition() {
            recognition = new (webkitSpeechRecognition || SpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;
            
            recognition.onresult = (event) => {
                const transcript = event.results[event.results.length - 1][0].transcript;
                document.getElementById('output').textContent += transcript;
            };
            
            recognition.onend = () => recognition.start();
            recognition.start();
        }
        
        function stopRecognition() {
            if (recognition) recognition.stop();
            document.getElementById('output').textContent = "";
        }
    </script>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start</button>
    <button id="end" onclick="stopRecognition()">Stop</button>
    <p id="output"></p>
</body>
</html>"""

# Write HTML file
with open(DATA_DIR / "Voice.html", "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def set_assistant_status(status: str) -> None:
    """Update assistant status file"""
    TEMP_DIR.mkdir(exist_ok=True)
    with open(TEMP_DIR / "Status.data", "w", encoding="utf-8") as f:
        f.write(status)

def query_modifier(query: str) -> str:
    """Format the query with proper punctuation"""
    query = query.lower().strip()
    if not query:
        return ""
    
    question_words = {"how", "what", "when", "where", "why", "who", 
                     "which", "whom", "whose", "can you", "what's", 
                     "how's", "where's"}
    
    is_question = any(query.startswith(word) for word in question_words)
    last_char = query[-1] if query else ""
    
    if last_char in {".", "?", "!"}:
        query = query[:-1]
    
    return f"{query}{'?' if is_question else '.'}".capitalize()

def universal_translator(text: str) -> str:
    """Translate text to English if needed"""
    if not text:
        return ""
    
    if "en" in INPUT_LANGUAGE:
        return text.capitalize()
    return mt.translate(text, "en", "auto").capitalize()

def speech_recognition() -> str:
    """Capture speech input and return processed text"""
    driver.get(f"file://{Path().absolute() / DATA_DIR / 'Voice.html'}")
    driver.find_element(By.ID, "start").click()
    
    while True:
        try:
            text = driver.find_element(By.ID, "output").text
            if text:
                driver.find_element(By.ID, "end").click()
                return query_modifier(universal_translator(text))
        except Exception:
            continue

if __name__ == "__main__":
    try:
        while True:
            print(speech_recognition())
    finally:
        driver.quit()