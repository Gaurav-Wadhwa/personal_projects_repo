import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import ssl
# Fix SSL issues
ssl._create_default_https_context = ssl._create_unverified_context
# Streamlit App Setup
st.set_page_config(page_title="Language Translator", page_icon="🌎")
st.title("🌎 Language Translator")
# Load Supported Languages
try:
    language_codes = GoogleTranslator().get_supported_languages(as_dict=True)
    language_names = list(language_codes.keys())
    default_lang_index = language_names.index("English") if "English" in language_names else 0
except Exception as e:
    st.error(f"Error loading languages: {e}")
    language_names = ["English", "Hindi", "French", "Spanish"]
    language_codes = {"English": "en", "Hindi": "hi", "French": "fr", "Spanish": "es"}
    default_lang_index = 0
# 🎤 Function to Convert Speech to Text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "❌ Could not understand the audio."
        except sr.RequestError:
            return "❌ Speech Recognition API error."
    return ""
# 🔊 Function to Convert Text to Speech
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio_path = temp_audio.name
        tts.save(temp_audio_path)
        st.audio(temp_audio_path, format="audio/mp3")
# 🎤 Speech Input Button
if st.button("🎤 Speak"):
    spoken_text = speech_to_text()
    st.text_area("Converted Text:", spoken_text, height=100)
# 📝 Manual Text Input
text_to_translate = st.text_area("Enter Text to Translate", spoken_text if "spoken_text" in locals() else "", height=100)
# 🔄 Language Selection Dropdowns
source_lang_name = st.selectbox("🔄 Source Language", ["Auto Detect"] + language_names)
target_lang_name = st.selectbox("🎯 Target Language", language_names, index=default_lang_index)
# Convert Language Names to Codes
source_lang = "auto" if source_lang_name == "Auto Detect" else language_codes.get(source_lang_name, "en")
target_lang = language_codes.get(target_lang_name, "en")
# 🔁 Translation Button
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        try:
            translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text_to_translate)
            st.success("✅ Translation:")
            st.write(translated_text)
            if st.button("🔊 Listen to Translation"):
                text_to_speech(translated_text, target_lang)
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.warning("⚠️ Please enter text.")
