import streamlit as st 
from googletrans import Translator, LANGUAGES
import ssl
# Fix SSL issues
ssl._create_default_https_context = ssl._create_unverified_context
# Initialize Translator
translator = Translator()
# Streamlit App Setup
st.set_page_config(page_title="Language Translator", page_icon="🌎")
st.write("### 🌎 Language Translator")
# 📝 Manual Text Input
text_to_translate = st.text_area("Enter Text to Translate", height=100)
# 🔄 Language Selection
language_names = list(LANGUAGES.values())  # Get language names
language_codes = {v: k for k, v in LANGUAGES.items()}  # Map names to codes
# Initialize session state for language selection
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "Auto Detect"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "english"
col1, col2, col3 = st.columns([3, 1, 3])
with col1:
    source_lang_name = st.selectbox("🔄 Source Language", ["Auto Detect"] + language_names, 
                                    index=(language_names.index(st.session_state.source_lang) 
                                    if st.session_state.source_lang in language_names else 0))
with col2:
    swap_pressed = st.button("🔄 Swap")
with col3:
    target_lang_name = st.selectbox("🎯 Target Language", language_names, 
                                    index=language_names.index(st.session_state.target_lang))
# Swap functionality
if swap_pressed:
    if source_lang_name != "Auto Detect":  # Prevent swapping when source is "Auto Detect"
        st.session_state.source_lang, st.session_state.target_lang = (
            st.session_state.target_lang, st.session_state.source_lang
        )
        st.experimental_rerun()  # Rerun the app to reflect the changes
# Update session state only when the user manually selects a language
st.session_state.source_lang = source_lang_name
st.session_state.target_lang = target_lang_name
# Convert Language Names to Codes
source_lang = "auto" if st.session_state.source_lang == "Auto Detect" else language_codes[st.session_state.source_lang]
target_lang = language_codes[st.session_state.target_lang]
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
