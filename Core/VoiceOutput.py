import os
import random
import asyncio
import pygame
import edge_tts
from pathlib import Path
from dotenv import dotenv_values

# Configuration
config = dotenv_values(".env")
VOICE = config.get("AssistantVoice", "en-US-GuyNeural")
DATA_DIR = Path("Data")
DATA_DIR.mkdir(exist_ok=True)
AUDIO_FILE = DATA_DIR / "Speech.mp3"

# Predefined responses
RESPONSES = [
    "The rest of the result has been printed to the chat screen, kindly check it out sir.",
    "The rest of the text is now on the chat screen, sir, please check it.",
    "You can see the rest of the text on the chat screen, sir.",
    "The remaining part of the text is now on the chat screen, sir.",
    "Sir, you'll find more text on the chat screen for you to see."
]

async def generate_audio(text: str) -> None:
    """Generate audio file from text using edge_tts"""
    if AUDIO_FILE.exists():
        AUDIO_FILE.unlink()
    
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        pitch="+5Hz",
        rate="+13%"
    )
    await communicate.save(str(AUDIO_FILE))

def play_audio(callback=lambda: True) -> bool:
    """Play the generated audio file"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(str(AUDIO_FILE))
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            if not callback():
                break
            pygame.time.Clock().tick(10)
        return True
    except Exception as e:
        print(f"Audio playback error: {e}")
        return False
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def text_to_speech(text: str, callback=lambda: True) -> None:
    """Convert text to speech with intelligent truncation"""
    if not text:
        return
    
    # For long texts, play the first part and notify about the rest
    if len(text.split()) > 4 and len(text) >= 250:
        sentences = text.split(".")
        partial_text = ".".join(sentences[:2]) + "." if len(sentences) > 2 else text
        full_text = f"{partial_text} {random.choice(RESPONSES)}"
    else:
        full_text = text
    
    # Generate and play audio
    asyncio.run(generate_audio(full_text))
    play_audio(callback)

if __name__ == "__main__":
    while True:
        text_to_speech(input("Enter the text: "))