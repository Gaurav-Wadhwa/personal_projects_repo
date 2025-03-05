import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import os
st.set_page_config(page_icon="🌎")
st.write("### 🌎 Language Translator")
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now")
            recognizer.adjust_for_ambient_noise(source)  # Helps with background noise
            audio = recognizer.listen(source, timeout=5)
            
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Speech Recognition API error"
    except OSError:
        return "Microphone not available (if running on a server, try file upload instead)"
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = "output.mp3"
    tts.save(filename)
    
    # Play the audio file
    if os.name == "nt":  # Windows
        os.system(f"start {filename}")
    else:  # macOS/Linux
        os.system(f"mpg321 {filename} &")
# Initialize spoken_text to avoid errors
spoken_text = ""
if st.button("🎤 Speak"):
    spoken_text = speech_to_text()
    st.text_area("Converted Text:", spoken_text)
text_to_translate = st.text_area("Enter text to translate", spoken_text)
# Get supported languages
languages = GoogleTranslator().get_supported_languages()
source_lang = st.selectbox("Enter Source Language", ["auto"] + languages)
target_lang = st.selectbox("Select Target Language", languages, index=languages.index("english"))
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text_to_translate)
        st.success("Translation:")
        st.write(translated_text)
        if st.button("🔊 Listen to Translation"):
            text_to_speech(translated_text, target_lang)
    else:
        st.warning("Please enter text or use speech input.")
