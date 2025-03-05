import streamlit as st
from googletrans import Translator, LANGUAGES
import ssl
# Fix SSL issues
ssl._create_default_https_context = ssl._create_unverified_context
# Initialize Translator
translator = Translator()
# Streamlit App Setup
st.set_page_config(page_title="Language Translator", page_icon="🌎")
st.title("### 🌎 Language Translator & Transliterator")
# 📝 Manual Text Input
text_to_translate = st.text_area("Enter Text to Translate", height=100)
# 🔄 Language Selection
language_names = list(LANGUAGES.values())  # Get language names
language_codes = {v: k for k, v in LANGUAGES.items()}  # Map names to codes
source_lang_name = st.selectbox("🔄 Source Language", ["Auto Detect"] + language_names)
target_lang_name = st.selectbox("🎯 Target Language", language_names, index=language_names.index("english"))
# Convert Language Names to Codes
source_lang = "auto" if source_lang_name == "Auto Detect" else language_codes[source_lang_name]
target_lang = language_codes[target_lang_name]
# 🔁 Translation & Transliteration
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        try:
            # ✅ Perfect Translation & Transliteration
            translated = translator.translate(text_to_translate, src=source_lang, dest=target_lang)
            st.success("✅ Translation:")
            st.write(translated.text)  # Proper translation
            
            # Transliteration (if available)
            if translated.pronunciation:
                st.info(f"🔠 Transliteration: {translated.pronunciation}")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.warning("⚠️ Please enter text.")
