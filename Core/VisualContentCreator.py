
import asyncio
import logging
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep
import re
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("debug.log")]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
HUGGING_FACE_API_KEY = os.getenv("HuggingFaceAPIKey")
if not HUGGING_FACE_API_KEY:
    logger.error("HUGGING_FACE_API_KEY not found in .env file")
    raise ValueError("HUGGING_FACE_API_KEY not found in .env file")

# API configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_HEADERS = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

# Paths
IMAGE_DIRECTORY = "Data"
REQUEST_FILE_PATH = os.path.join("Data", "image.data")

def ensure_directory(directory: str):
    """Ensures the specified directory exists."""
    try:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        raise

def display_images(image_prompt: str):
    """Opens and displays images based on the given prompt."""
    image_prompt = image_prompt.replace(" ", "_")
    image_filenames = [f"{image_prompt}{i}.jpg" for i in range(1, 5)]
    logger.debug(f"Generated filenames: {image_filenames}")

    for image_file in image_filenames:
        file_path = os.path.join(IMAGE_DIRECTORY, image_file)
        try:
            img = Image.open(file_path)
            print(f"Opening image: {file_path}")
            logger.info(f"Opening image: {file_path}")
            img.show()
        except IOError as e:
            print(f"Unable to open {file_path}")
            logger.warning(f"Unable to open {file_path}: {e}")

async def fetch_image_from_api(payload: dict, max_retries: int = 3) -> bytes:
    """Fetches an image from the Hugging Face API with retries."""
    for attempt in range(1, max_retries + 1):
        try:
            logger.debug(f"API call attempt {attempt} with payload: {payload}")
            response = await asyncio.to_thread(
                requests.post, API_URL, headers=API_HEADERS, json=payload
            )
            response.raise_for_status()
            logger.debug(f"API response status: {response.status_code}")
            return response.content
        except requests.RequestException as e:
            logger.warning(f"API call attempt {attempt} failed: {e}")
            if response.status_code == 400:
                try:
                    error_details = response.json()
                    logger.error(f"API error details: {error_details}")
                except json.JSONDecodeError:
                    logger.error(f"API error response: {response.text}")
            if attempt < max_retries:
                logger.info("Retrying after 5 seconds...")
                await asyncio.sleep(5)
            else:
                logger.error(f"Max retries reached for API call: {e}")
                return b""

async def generate_image_set(image_prompt: str):
    """Generates a set of images for the given prompt."""
    if not is_valid_prompt(image_prompt):
        logger.warning(f"Invalid prompt: {image_prompt}")
        return

    # Sanitize prompt to avoid copyrighted terms
    sanitized_prompt = re.sub(r"iron man", "futuristic armored hero", image_prompt, flags=re.IGNORECASE)
    logger.debug(f"Sanitized prompt: {sanitized_prompt}")

    enhanced_prompt = (
        f"{sanitized_prompt}, 8K resolution, photorealistic, cinematic lighting, "
        f"vibrant colors, ultra-detailed textures, maximum sharpness, professional studio quality"
    )
    logger.debug(f"Enhanced prompt: {enhanced_prompt}")

    image_tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{enhanced_prompt}, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(fetch_image_from_api(payload))
        image_tasks.append(task)

    image_data_list = await asyncio.gather(*image_tasks)
    logger.debug(f"Received {len(image_data_list)} image data entries")

    ensure_directory(IMAGE_DIRECTORY)
    for i, image_data in enumerate(image_data_list):
        if image_data:
            file_path = os.path.join(IMAGE_DIRECTORY, f"{image_prompt.replace(' ', '_')}{i + 1}.jpg")
            try:
                with open(file_path, "wb") as file:
                    file.write(image_data)
                logger.info(f"Saved image: {file_path}")
            except IOError as e:
                logger.error(f"Failed to save image {file_path}: {e}")
        else:
            logger.warning(f"No image data for {image_prompt}_{i + 1}.jpg")

def create_and_show_images(image_prompt: str):
    """Generates and displays images for the given prompt."""
    print("Generating Images ...")
    logger.info(f"Generating images for prompt: {image_prompt}")
    asyncio.run(generate_image_set(image_prompt))
    display_images(image_prompt)

def is_valid_prompt(prompt: str) -> bool:
    """Validates the prompt to ensure it's not empty or command-line-like."""
    valid = bool(prompt.strip()) and not re.match(r".*[\\/].*\.exe|.*[\\/].*\.py|&.*", prompt)
    logger.debug(f"Prompt validation: '{prompt}' is {'valid' if valid else 'invalid'}")
    return valid

def main():
    """Monitors the request file for image generation tasks."""
    logger.info("Starting Jarvis image generation monitor")
    ensure_directory(os.path.dirname(REQUEST_FILE_PATH))
    while True:
        try:
            with open(REQUEST_FILE_PATH, "r") as file:
                file_content = file.read().strip()
            if not file_content:
                logger.debug("Request file is empty, waiting...")
                sleep(1)
                continue

            logger.debug(f"Read file content: {file_content}")
            user_prompt, request_status = file_content.split(",")
            logger.debug(f"Parsed prompt: '{user_prompt}', status: '{request_status}'")
            if request_status.strip().lower() == "true" and is_valid_prompt(user_prompt):
                logger.info("Image generation request detected")
                create_and_show_images(user_prompt.strip())
                with open(REQUEST_FILE_PATH, "w") as file:
                    file.write(f"{user_prompt.strip()},False")
                logger.info("Request processed, status reset to False")
                break
            else:
                logger.debug(f"No action: status='{request_status.strip()}', valid_prompt={is_valid_prompt(user_prompt)}")
                sleep(1)
        except FileNotFoundError:
            logger.warning(f"Request file not found: {REQUEST_FILE_PATH}")
            sleep(1)
        except ValueError:
            logger.warning(f"Invalid file format in {REQUEST_FILE_PATH}: {file_content}")
            sleep(1)
        except IOError as e:
            logger.error(f"File access error: {e}")
            sleep(1)

if __name__ == "__main__":
    main()
