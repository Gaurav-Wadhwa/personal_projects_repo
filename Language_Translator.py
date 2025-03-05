import streamlit as st
from deep_translator import GoogleTranslator
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
# 📝 Manual Text Input
text_to_translate = st.text_area("Enter Text to Translate", height=100)
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
            # ✅ Fix for transliteration: Always use `auto` detection
            translated_text = GoogleTranslator(source="auto", target=target_lang).translate(text_to_translate)
            st.success("✅ Translation:")
            st.write(translated_text)
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.warning("⚠️ Please enter text.")
