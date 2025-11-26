import os
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
import time
import tempfile
from config.interview_data import (
    CANDIDATE_NAME,
    CANDIDATE_BACKGROUND,
    INTERVIEW_ANSWERS,
    PROJECTS,
    PERSONALITY,
    get_system_prompt
)

# Page configuration
st.set_page_config(
    page_title=f"Interview with {CANDIDATE_NAME}",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #000000;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .bot-message {
        background-color: #f1f8e9;
        border-left: 5px solid #8bc34a;
    }
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        white-space: nowrap;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = None
if "audio_processed" not in st.session_state:
    st.session_state.audio_processed = False


def initialize_gemini():
    """Initialize Gemini API client"""
    try:
        api_key = st.secrets["google"]["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.session_state.gemini_client = model
        return True
    except Exception as e:
        st.error(f"Failed to initialize Gemini API: {str(e)}")
        return False

def generate_ai_response(user_question):
    """Generate AI response using Gemini"""
    try:
        if st.session_state.gemini_client is None:
            if not initialize_gemini():
                return "Sorry, I'm having trouble connecting to the AI service."
        
        # Build context from interview data
        system_prompt = get_system_prompt()
        
        # Create conversation context
        conversation_context = f"{system_prompt}\n\nUser Question: {user_question}\n\nAnswer as Amarthya would:"
        
        # Generate response
        response = st.session_state.gemini_client.generate_content(conversation_context)
        
        return response.text
    
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return "I apologize, but I'm having trouble processing that question right now."

def text_to_speech(text):
    """Convert text to speech using gTTS"""
    try:
        # Create TTS object
        tts = gTTS(text=text, lang='en', slow=False, tld="co.in")
        
        # Save to BytesIO object
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        return audio_fp
    except Exception as e:
        st.error(f"Error converting text to speech: {str(e)}")
        return None

def main():
    # Header
    st.markdown(f'<div class="main-header"> AI Interview Bot</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Interview with {CANDIDATE_NAME}</div>', unsafe_allow_html=True)
    
    # Initialize Gemini on first run
    if st.session_state.gemini_client is None:
        with st.spinner("Initializing AI..."):
            initialize_gemini()
    
    # Sidebar with instructions and info
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Type your question** in the text box below
        2. Click **"Ask Question"** to get a response
        3. Listen to the **audio response**
        4. View the **chat history** below
        
        ### Sample Questions:
        - What should we know about your life story?
        - What's your #1 superpower?
        - What are your top 3 growth areas?
        - What misconception do people have about you?
        - How do you push your boundaries?
        """)
        
        st.divider()
        
        st.header("👤 About")
        st.markdown(f"**Name:** {CANDIDATE_NAME}")
        st.markdown(f"**Background:** MTech from IIT Madras")
        st.markdown(f"**Other Interests:** {', '.join(PERSONALITY['interests'][:4])}")
        
        st.divider()
        
        if st.button("🔄 Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")
    
    # Voice Input Section
    st.markdown("### Voice Input (Optional):")
    audio_input_live = st.audio_input("Record Your Question and Press Submit")

    # Only process audio once
    if audio_input_live and not st.session_state.audio_processed:
        audio_bytes = audio_input_live.getvalue()

        if len(audio_bytes) > 1000:
            with st.spinner("🎧 Transcribing audio..."):
                try:
                    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav', mode='wb')
                    temp_wav.write(audio_bytes)
                    temp_wav.flush()
                    temp_wav_path = temp_wav.name
                    temp_wav.close()

                    recognizer = sr.Recognizer()
                    with sr.AudioFile(temp_wav_path) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio_data = recognizer.record(source)
                        transcribed_text = recognizer.recognize_google(audio_data)

                    os.unlink(temp_wav_path)

                    st.session_state.voice_input_text = transcribed_text
                    st.session_state.audio_processed = True  # IMPORTANT FIX
                    st.success(f"✅ Transcribed: {transcribed_text}")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Transcription failed: {e}")
                    try:
                        os.unlink(temp_wav_path)
                    except:
                        pass
        else:
            st.warning("⚠️ Audio too short. Please record again.")

    st.markdown("---")
    
    # Main question input form
    with st.form(key='question_form', clear_on_submit=False):
        default_question = ""
        if 'voice_input_text' in st.session_state:
            default_question = st.session_state.voice_input_text
            st.session_state.question_input = st.session_state.voice_input_text
        elif 'selected_question' in st.session_state:
            default_question = st.session_state.selected_question
        
        user_question = st.text_input(
            "💬 Type your question:",
            value=default_question,
            placeholder="e.g., What's your #1 superpower?",
            key="question_input"
        )
        
        ask_button = st.form_submit_button(" Ask Question (or press Enter)", type="primary", use_container_width=True)
        
        if ask_button and user_question.strip():
            with st.spinner("🤔 Thinking..."):
                ai_response = generate_ai_response(user_question)
                audio_data = text_to_speech(ai_response)
                
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": ai_response,
                    "timestamp": time.strftime("%H:%M:%S"),
                    "audio": audio_data
                })
                
                # Clear session state
                if 'voice_input_text' in st.session_state:
                    del st.session_state.voice_input_text
                if 'selected_question' in st.session_state:
                    del st.session_state.selected_question

                # Reset so next voice recording will be processed
                st.session_state.audio_processed = False
                
                st.markdown("### Response:")
                st.markdown(f'<div class="chat-message bot-message">{ai_response}</div>', unsafe_allow_html=True)
                
                if audio_data:
                    st.audio(audio_data, format='audio/mp3', autoplay=False)
                    st.caption("🔊 Click play to hear the response")
    
    # Display chat history
    if st.session_state.chat_history:
        st.divider()
        st.markdown("### 💬 Conversation History")
        
        for chat in st.session_state.chat_history:
            st.markdown(f"""
            <div style='background-color: #e3f2fd; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; border-left: 5px solid #2196f3; color: #000000'>
                <strong>🧑 You ({chat['timestamp']}):</strong><br>
                {chat['question']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='background-color: #f1f8e9; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 5px solid #8bc34a; color: #000000'>
                <strong>🤖 Amarthya:</strong><br>
                {chat['answer']}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            with col2:
                if chat["audio"]:
                    st.audio(chat["audio"], format='audio/mp3', autoplay=False)
            
            st.markdown("---")
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #888; padding: 1rem;'>
            Built with ❤️ using Streamlit & Google Gemini | 
            <a href='mailto:amarthyapramodk@gmail.com'>Contact</a> | 
            <a href='https://github.com/amarthyapramod'>GitHub</a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
