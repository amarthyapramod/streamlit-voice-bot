# 🎤 AI Voice Interview Bot - Amarthya Pramod K

> A fully voice-enabled AI interview assistant that listens to questions, transcribes them, generates responses using Google Gemini, and speaks them back using fast TTS.

## 🎯 Project Overview

This AI-powered interview bot conducts interactive voice interviews, answering questions authentically as Amarthya Pramod K. It demonstrates:

✅ **Natural Language Understanding** - Processes interview questions intelligently  
✅ **Personalized AI Responses** - Answers reflect real experiences, projects, and personality  
✅ **Voice Input** - Speak your question → app records → converts → transcribes → answers.
✅ **Text-to-Speech Output** - Converts responses to natural-sounding voice  
✅ **Clean Web Interface** - User-friendly Streamlit application  
✅ **Production-Ready** - Deployed and accessible via web URL

## 🚀 Live Demo

**[Try it live here!](#)** 

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web interface and UI 
| **AI Model** | Google Gemini 1.5 Flash | Natural language generation |
| **Voice Input** | Streamlit- audiorecorder | Browser microphone recording |
| **Speech-to-text** | Google Gemini Audio Transcription | Converts voice to text |
| **Text-to-Speech** | gTTS (Google TTS) | converts answers to speech |
| **Deployment** | Streamlit Cloud | Free hosting |

---

## 📋 Features

### Core Functionality
- ⚡ **Voice Input** - Records user's voice from browser and responds
- 🎤 **Voice Output** - AI responses converted to natural speech
- 💬 **Chat Interface** - Clean, intuitive conversation UI
- 📜 **Chat History** - View and replay previous Q&A
- 🎨 **Custom Styling** - Professional, modern design

### AI Capabilities
- **Context-Aware Responses** - Understands interview context
- **Personalized Content** - Answers based on real background and projects
- **Natural Conversation** - Maintains Amarthya's authentic style
- **Technical Depth** - Can discuss projects, technologies, and experiences in detail

### Interview Topics Covered
1. Life story and background
2. Key strengths and superpowers
3. Growth areas and learning goals
4. Common misconceptions
5. Overcoming challenges and pushing boundaries

---

## 📂 Project Structure

```
voice-interview-bot/
│
├── 📄 app.py                          # Main Streamlit application
├── 📄 requirements.txt                # Python dependencies
├── 📄 .gitignore                      # Git ignore rules
├── 📄 README.md                       # This file
│
├── 📂 .streamlit/
│   ├── 📄 secrets.toml               # API keys (NOT committed)
│   └── 📄 secrets.toml.example       # Template for API keys
│
└── 📂 config/
    └── 📄 interview_data.py          # Interview content and answers
```

---

## 🏃 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/amarthyapramod/voice-interview-bot.git
cd voice-interview-bot

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up API key
# Create .streamlit folder and secrets.toml file
mkdir .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit .streamlit/secrets.toml and add your Gemini API key:
# [google]
# GEMINI_API_KEY = "your_actual_api_key_here"

# 6. Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 💡 Usage

### Asking Questions

1. **Record or Type your question** Using Voice input feature(optional) or type in the text input field
2. **Click "Ask Question"** button or press enter
3. **View the response** in text format
4. **Listen to audio** response automatically generated. press play to head response
5. **Check chat history** to review previous answers

### Sample Questions

Try these interview questions:

- *"What should we know about your life story in a few sentences?"*
- *"What's your #1 superpower?"*
- *"What are the top 3 areas you'd like to grow in?"*
- *"What misconception do your coworkers have about you?"*
- *"How do you push your boundaries and limits?"*


---

## 🧠 How It Works

### Architecture Flow

```
User Speaks or Types a Question
        ↓
Browser Records Audio (via audio_recorder_streamlit)
        ↓
Audio Saved Locally as WAV
        ↓
Gemini Audio Transcription (Speech-to-Text)
        ↓
Final Text Question Sent to Gemini LLM
        ↓
Gemini API (with context from interview_data.py)
        ↓
AI-Generated Response (as Amarthya)
        ↓
gTTS (Fast Text-to-Speech Conversion)
        ↓
Audio Output + Text Display in Streamlit
```

### Key Components

**1. Voice Input System (Microphone Recording → WAV)**
- Uses audio_recorder_streamlit to capture microphone audio
- Ensures audio bytes are properly saved (fixed silence/blank audio issues)
- Converts browser-recorded format to clean .wav using FFmpeg
- Passes WAV file to Gemini for speech-to-text

**2. Context System (`config/interview_data.py`)**
- Stores detailed background, projects, skills, personality traits
- Provides system prompt to guide Gemini's responses
- Ensures consistency and authenticity in answers

**3. AI Generation (`app.py`)**
- Sends questions with full context to Gemini
- Generates personalized responses as Amarthya
- Maintains conversation history for context

**4. Voice Output**
- Converts AI text responses to speech using gTTS
- Plays audio directly in browser
- Downloadable audio for each response

---
## 🎓 Technical Highlights

### Production-Ready Features

✅ **Reliable Voice input** - stable audio recording pipeline using WAV + FFmpeg
✅ **Accurate Speech-to-Text** — Gemini 1.5 Flash audio transcription
✅ **Fast TTS Output** — accelerated gTTS voice playback
✅ **Error Handling** — graceful fallback if recording fails
✅ **Session Management** — persistent chat history and audio logs
✅ **Security** — API key stored only in Streamlit Secrets
✅ **Performance** — optimized API calls, controlled processing
✅ **User Experience** — clean UI, progress indicators, retry mechanisms
✅ **Scalability** — runs seamlessly on Streamlit Cloud

### Code Quality

- **Modular Architecture** — prompts, UI, LLM logic separated
- **Robust Audio Handling** — consistent WAV creation, no empty buffers
- **Clean State Management** — predictable Streamlit session behavior
- **Inline Documentation** — readable, production-ready code

- **Best Practices** — proper secrets handling, minimal API calls, safe temp files
---

## 🔒 Security & Privacy

- ✅ API keys stored in Streamlit secrets (encrypted)
- ✅ `.gitignore` prevents credential leaks
- ✅ No personal data collected from users
- ✅ Secure HTTPS deployment on Streamlit Cloud

---

## 🚀 Future Enhancements

Potential improvements for v2.0:

- [ ] **Multi-language Support** - Answer in multiple languages
- [ ] **Advanced Analytics** - Track common questions and engagement
- [ ] **Custom Voice** - Train on actual voice samples
- [ ] **Video Avatar** - Add visual representation
- [ ] **Database Integration** - Store conversation history
- [ ] **Admin Dashboard** - View usage statistics

---

**Built by Amarthya Pramod K**

*Last Updated: November 2025*
