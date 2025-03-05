import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import ssl
# Fix SSL issues
ssl._create_default_https_context = ssl._create_unverified_context
# Streamlit App Setup
st.set_page_config(page_title="Language Translator", page_icon="🌎")
st.title("🌎 Language Translator")
# Speech-to-Text Function (Uses `pydub` Instead of `pyaudio`)
def speech_to_text():
    recognizer = sr.Recognizer()
    
    # Load a default audio file (since microphone input is not supported on Streamlit Cloud)
    uploaded_file = st.file_uploader("Upload an audio file (WAV/MP3)", type=["wav", "mp3"])
    
    if uploaded_file:
        audio_path = f"temp_audio.{uploaded_file.name.split('.')[-1]}"
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Convert MP3 to WAV if needed
        if audio_path.endswith(".mp3"):
            sound = AudioSegment.from_mp3(audio_path)
            audio_path = "temp_audio.wav"
            sound.export(audio_path, format="wav")
        
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                os.remove(audio_path)  # Clean up
                return text
            except sr.UnknownValueError:
                return "❌ Could not understand the audio."
            except sr.RequestError:
                return "❌ Speech Recognition API error."
    return ""
# Text-to-Speech Function
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = "output.mp3"
    tts.save(filename)
    st.audio(filename, format="audio/mp3")  # Play audio in Streamlit
# Load Supported Languages
try:
    language_codes = GoogleTranslator().get_supported_languages(as_dict=True)
    language_names = list(language_codes.keys())
    default_lang_index = language_names.index("English") if "English" in language_names else 0
except Exception as e:
    st.error(f"Error loading languages: {e}")
    language_names = ["English", "Hindi", "French", "Spanish"]  # Fallback languages
    language_codes = {"English": "en", "Hindi": "hi", "French": "fr", "Spanish": "es"}
    default_lang_index = 0
# Speech Input Button (Uses File Upload Instead of Microphone)
spoken_text = speech_to_text()
if spoken_text:
    st.text_area("Converted Text:", spoken_text, height=100)
# Manual Text Input
st.subheader("📝 Enter Text to Translate")
text_to_translate = st.text_area("Enter text:", spoken_text, height=100)
# Language Selection Dropdowns
source_lang_name = st.selectbox("🔄 Source Language", ["Auto Detect"] + language_names)
target_lang_name = st.selectbox("🎯 Target Language", language_names, index=default_lang_index)
# Convert Language Names to Codes
source_lang = "auto" if source_lang_name == "Auto Detect" else language_codes.get(source_lang_name, "en")
target_lang = language_codes.get(target_lang_name, "en")
# Translation Button
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text_to_translate)
        st.success("✅ Translation:")
        st.write(translated_text)
        if st.button("🔊 Listen to Translation"):
            text_to_speech(translated_text, target_lang)
    else:
        st.warning("⚠️ Please enter text or upload an audio file.")
