import streamlit as st
from google.cloud import translate_v2 as translate
import os
# ✅ Set up Google Cloud API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-google-cloud-key.json"
# ✅ Initialize Translator
translate_client = translate.Client()
# 🌎 Streamlit App
st.set_page_config(page_title="Advanced Translator", page_icon="🌍")
st.write("### 🌍 Language Translator & Transliterator")
# 📝 Text Input
text_to_translate = st.text_area("Enter Text to Translate", height=100)
# 🔄 Language Selection
languages = translate_client.get_languages()
language_names = [lang["name"] for lang in languages]
language_codes = {lang["name"]: lang["language"] for lang in languages}
source_lang_name = st.selectbox("🔄 Source Language", ["Auto Detect"] + language_names)
target_lang_name = st.selectbox("🎯 Target Language", language_names, index=language_names.index("English"))
# Convert Language Names to Codes
source_lang = "auto" if source_lang_name == "Auto Detect" else language_codes[source_lang_name]
target_lang = language_codes[target_lang_name]
# 🔁 Translation & Transliteration
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        try:
            # ✅ Perfect Translation
            result = translate_client.translate(text_to_translate, source_language=source_lang, target_language=target_lang)
            st.success("✅ Translation:")
            st.write(result["translatedText"])
            # ✅ Accurate Transliteration (if available)
            if "transliteration" in result:
                st.info(f"🔠 Transliteration: {result['transliteration']}")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.warning("⚠️ Please enter text.")
