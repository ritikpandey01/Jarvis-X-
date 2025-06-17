# 🤖 Jarvis - Advanced AI Chatbot Assistant

## 📋 Overview
Jarvis is an advanced AI-powered chatbot assistant designed to handle a variety of tasks such as answering queries, performing real-time searches, generating images, executing system tasks, and providing voice-based interactions. Built with a modular architecture, Jarvis leverages APIs like Groq and Hugging Face, along with libraries like PyQt5, Selenium, and edge-tts for a seamless user experience.

> **⚠️ Status:** Currently in active development with new features being added regularly.

## ✨ Features

- 💬 **Conversational AI** - Answer general and real-time queries using the Groq API
- 🔍 **Real-Time Search** - Fetch up-to-date information using Google Search
- ⚙️ **Task Automation** - Open/close applications, play music on YouTube, perform system tasks (mute, volume control, etc.)
- 🎨 **Image Generation** - Generate images using Hugging Face's Stable Diffusion model
- 🎤 **Voice Interaction** - Support for voice input (via Selenium-based speech recognition) and voice output (via edge-tts)
- 🖥️ **Graphical Interface** - A PyQt5-based GUI for user interaction
- 📝 **Chat History** - Maintains conversation logs for reference
- ⚙️ **Customizable** - Configurable via .env file for usernames, API keys, and other settings

## 📋 Prerequisites

- 🐍 Python 3.9 or higher
- 🌐 Internet access
- 🌍 Google Chrome (for Selenium-based voice input)
- 🔑 API keys for:
  - **Groq API** (`GROQ_API_KEY`)
  - **Hugging Face API** (`HUGGING_FACE_API_KEY`)

## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd jarvis-x
```

### 2️⃣ Set Up Virtual Environment *(recommended)*
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

**📦 Required packages include:**
```
groq, googlesearch-python, AppOpener, pywhatkit, requests
beautifulsoup4, rich, keyboard, PyQt5, selenium, webdriver-manager
mtranslate, Pillow, edge-tts, pygame
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the project root:
```env
Username=YourName
Assistantname=Jarvis
GroqAPIKey=your-groq-api-key
HuggingFaceAPIKey=your-hugging-face-api-key
InputLanguage=en
AssistantVoice=en-US-GuyNeural
```

### 5️⃣ Setup Complete! 
The project automatically creates a `Data` directory to store logs, chat history, and generated content.

## 🎯 Usage

### 🏃‍♂️ Run the Application
```bash
python main.py
```

### 🗣️ Interact with Jarvis
- A GUI window will appear with a microphone button to toggle voice input
- Speak or type your query (if voice input is disabled)
- Jarvis will classify your query and perform the appropriate action
- Use activation commands to control voice input

### 🎮 Voice Control Commands
| Command | Action |
|---------|--------|
| `"Jarvis, wake up"` | Activate voice input |
| `"Jarvis, sleep"` | Deactivate voice input |

### 💡 Example Commands

| Category | Example Command |
|----------|----------------|
| 📚 **General Query** | *"Who was Akbar?"* |
| 🌐 **Real-time Query** | *"Who is the current Indian Prime Minister?"* |
| 🚀 **Open Application** | *"Open Chrome"* |
| 🎵 **Play Music** | *"Play Let Her Go"* |
| 🎨 **Generate Image** | *"Generate image of a futuristic armored hero"* |
| 🔧 **System Task** | *"Mute"* |

## 📁 Project Structure

```
jarvis/
├── 📂 Core/                           # Core functionality modules
│   ├── 🤖 ChatBot.py                 # Handles general query answering using Groq API
│   ├── 🔍 QueryClassifier.py         # Classifies user queries into task categories
│   ├── 🌐 RealTimeSearch.py          # Performs real-time searches using Google
│   ├── ⚙️ TaskExecuter.py            # Executes tasks like opening apps, playing music
│   ├── 🎤 VoiceInput.py              # Captures voice input using Selenium
│   ├── 🎨 VisualContentCreator.py    # Generates images using Hugging Face
│   └── 🔊 VoiceOutput.py             # Converts text to speech using edge-tts
├── 📂 Interface/                      # GUI-related files
│   └── 🖥️ UI.py                      # PyQt5-based graphical interface
├── 📂 Data/                          # Storage for logs and generated content
│   ├── 📋 assistant.log              # Application activity logs
│   ├── 💬 ChatLog.json              # Conversation history
│   ├── 📝 ConversationLog.json      # Additional conversation log
│   └── 🖼️ generated_images/         # Folder for AI-generated images
├── ▶️ main.py                        # Entry point of the application
├── ⚙️ .env                          # Configuration file for environment variables
├── 🐛 debug.log                     # Debug log file for image generation
└── 📦 requirements.txt              # List of required Python packages
```

## 📝 Important Notes

- 🎤 **Voice Input**: Requires Google Chrome for Selenium to work. Ensure ChromeDriver is compatible with your Chrome version
- 🎨 **Image Generation**: May take time depending on the Hugging Face API response. Generated images are saved in the Data directory
- 📊 **Error Handling**: Logs are stored in `Data/assistant.log` and `debug.log` for debugging purposes
- 🔧 **Customization**: Modify the `.env` file to change the assistant's name, voice, or input language

## 🛠️ Troubleshooting

### 🔑 API Key Issues
Ensure your Groq and Hugging Face API keys are valid and correctly set in the `.env` file.

### 🎤 Voice Input Not Working
- Check if Chrome is installed and ChromeDriver is compatible
- Ensure microphone access is granted
- Verify Selenium WebDriver setup

### 🖥️ GUI Not Displaying
- Verify PyQt5 installation: `pip install PyQt5`
- Check system display settings
- Try running: `python -c "import PyQt5; print('PyQt5 OK')"`

### 🎨 Image Generation Fails
- Check the `debug.log` file for API errors
- Ensure your Hugging Face API key has sufficient credits
- Verify internet connection stability

## 🤝 Contributing

This project is actively being developed and contributions are welcome! 

**How to contribute:**
1. Fork the project
2. Create your feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

For major changes, please open an issue first to discuss your ideas.

---

<div align="center">

**🚀 Built with ❤️ by [Ritik Pandey]**


</div>
