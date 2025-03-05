import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import os
st.set_page_config(page_title="Language Translator", page_icon="🌎")
st.title("🌎 Language Translator")
# Function to convert speech to text from an uploaded file
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    # Convert audio file to WAV format
    audio = AudioSegment.from_file(audio_file)
    converted_file = "converted.wav"
    audio.export(converted_file, format="wav")
    
    with sr.AudioFile(converted_file) as source:
        st.info("🎙️ Processing Audio...")
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
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
# UI for uploading an audio file
st.subheader("🎤 Upload an Audio File (WAV, MP3, OGG)")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])
spoken_text = ""
if uploaded_file is not None:
    spoken_text = speech_to_text(uploaded_file)
    st.text_area("Converted Text:", spoken_text)
# UI for manual text input
st.subheader("📝 Enter Text to Translate")
text_to_translate = st.text_area("Enter text:", spoken_text)
# Dropdowns for language selection
languages = GoogleTranslator().get_supported_languages()
source_lang = st.selectbox("🔄 Source Language", ["auto"] + languages)
target_lang = st.selectbox("🎯 Target Language", languages, index=languages.index("english"))
# Translation button
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text_to_translate)
        st.success("✅ Translation:")
        st.write(translated_text)
        if st.button("🔊 Listen to Translation"):
            text_to_speech(translated_text, target_lang)
    else:
        st.warning("⚠️ Please enter text or upload an audio file.")
