# 🚀 JARVIS - Your Personal AI Assistant

> "Just A Rather Very Intelligent System" - Your own Iron Man assistant!

A cool AI assistant that can talk, search, automate your PC, and much more. Built with Python and powered by voice recognition.


## 🎯 What Can JARVIS Do?

### 💬 Talk Like a Human
- Have normal conversations
- Ask anything - from jokes to complex questions
- Remembers your chat history
- Responds with voice (not just text!)

### 🔍 Real-Time Search
- Get latest news instantly
- Search Google for anything
- Find YouTube videos
- Weather updates and more

### 🤖 Control Your PC
- Open/close any app or website
- Launch system applications
- File and folder management
- Execute system commands
- Control media playback

### 🎨 Creative Helper
- Generate AI images
- Write code and save to Notepad
- Compose songs and poems
- Help with coding projects
- Create simple scripts

### 📝 Writing Assistant
- Write directly to Notepad
- Generate code snippets
- Create documentation
- Help with creative writing
- Auto-type responses

## 🎬 Quick Demo

```
You: "Hey JARVIS, what's the weather today?"
JARVIS: "Let me check the latest weather for you..."

You: "Write a Python calculator code in notepad"
JARVIS: "Opening notepad and writing the code for you!"

You: "Open YouTube and play some music"
JARVIS: "Opening YouTube and finding music!"

You: "Generate an image of a sunset"
JARVIS: "Creating that image... Done!"

You: "Close all browsers"
JARVIS: "Closing all browser windows!"
```

## ⚡ Quick Start

1. **Download & Install**
   ```bash
   git clone https://github.com/ritikpandey01/Jarvis-X-
   cd jarvis
   pip install -r requirements.txt
   ```

2. **Setup Your Details & API Keys**
   
   Create a `.env` file in the root directory:
   ```env
   # Personal Settings
   Username=YourName
   Assistantname=JARVIS
   InputLanguage=en
   AssistantVoice=en-CA-LiamNeural
   
   # Required API Keys (Get them from respective websites)
   CohereAPIKey=your_cohere_api_key_here
   GroqAPIKey=your_groq_api_key_here
   HuggingFaceAPIKey=your_huggingface_api_key_here
   ```

3. **Run JARVIS**
   ```bash
   python main.py
   ```

That's it! Your JARVIS is ready 🎉

## 📱 How to Use

### Voice Commands
- **"Hello JARVIS"** → Start chatting
- **"Search for [anything]"** → Real-time search  
- **"Open/Close [app name]"** → Control applications
- **"Write [language] code in notepad"** → Auto-code in notepad
- **"Generate image of [description]"** → AI image creation
- **"Play music"** → Media control
- **"Write me a song about [topic]"** → Creative writing

### Chat Features
- Ask questions about anything
- Get real-time information
- Creative writing help
- Coding assistance
- System automation

## 🛠️ What's Inside

```
JARVIS/
├── main.py              # Start here!
├── Frontend/GUI.py      # Cool interface
├── Backend/
│   ├── Chatbot.py      # Brain of JARVIS (Cohere AI)
│   ├── SpeechToText.py # Hears you
│   ├── TextToSpeech.py # Talks back
│   ├── Automation.py   # Controls your PC
│   ├── ImageGeneration.py # AI Images (HuggingFace)
│   └── RealTimeSearchEngine.py # Searches web
├── Data/ChatLog.json   # Remembers everything
├── .env                # Your API keys (keep secret!)
└── requirements.txt    # Dependencies
```

## 🎮 Cool Features

✅ **Voice Chat** - Talk naturally, no typing needed  
✅ **Smart Search** - Gets latest info from internet  
✅ **PC Automation** - Open/close apps, system control  
✅ **Code Helper** - Writes code directly in Notepad  
✅ **AI Images** - Creates images from descriptions  
✅ **Media Control** - Play music, manage files  
✅ **Creative Writing** - Songs, poems, stories  
✅ **Memory** - Remembers all conversations  
✅ **Multi-tasking** - Handles multiple requests  

## 🐛 Need Help?

**Common Issues:**
- **API Keys not working?** Check if they're correctly added to .env file
- **"API limit exceeded"?** You might need to upgrade your API plan
- **Microphone not working?** Check permissions in system settings
- **Voice too fast/slow?** Change AssistantVoice in .env file
- **App not opening?** Check automation permissions

## 🚀 Make It Better

Want to add features? Here's how:
1. Fork this repo
2. Add your cool feature
3. Test it out
4. Send a pull request


## 📞 Connect

Built with ❤️ by [Ritik Pandey]  
📧 Contact: your.ritikpandey.4161@gmail.com  
---

**Ready to feel like Tony Stark? Let's get JARVIS running! 🦾**
(https://github.com/ritikpandey01/Jarvis-X-)
