import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import os
import ssl
# Fix SSL certificate issue
ssl._create_default_https_context = ssl._create_unverified_context
st.set_page_config(page_title="Language Translator", page_icon="🌎")
st.title("🌎 Language Translator")
# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "❌ Could not understand the audio."
        except sr.RequestError:
            return "❌ Speech Recognition API error."
# Function to convert text to speech
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = "output.mp3"
    tts.save(filename)
    st.audio(filename, format="audio/mp3")  # Play audio in Streamlit
# Load supported languages
try:
    language_codes = GoogleTranslator().get_supported_languages(as_dict=True)
    language_names = list(language_codes.keys())
except Exception as e:
    st.error(f"Error loading languages: {e}")
    language_names = ["English", "Hindi", "French", "Spanish"]  # Fallback languages
    language_codes = {"English": "en", "Hindi": "hi", "French": "fr", "Spanish": "es"}
# Speech input button
if st.button("🎤 Speak"):
    spoken_text = speech_to_text()
    st.text_area("Converted Text:", spoken_text, height=100)
else:
    spoken_text = ""
# Manual text input
st.subheader("📝 Enter Text to Translate")
text_to_translate = st.text_area("Enter text:", spoken_text, height=100)
# Dropdowns for language selection
source_lang_name = st.selectbox("🔄 Source Language", ["Auto Detect"] + language_names)
target_lang_name = st.selectbox("🎯 Target Language", language_names, index=language_names.index("English"))
# Convert selected language names to language codes
source_lang = "auto" if source_lang_name == "Auto Detect" else language_codes.get(source_lang_name, "en")
target_lang = language_codes.get(target_lang_name, "en")
# Translation button
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text_to_translate)
        st.success("✅ Translation:")
        st.write(translated_text)
        if st.button("🔊 Listen to Translation"):
            text_to_speech(translated_text, target_lang)
    else:
        st.warning("⚠️ Please enter text or use speech input.")
