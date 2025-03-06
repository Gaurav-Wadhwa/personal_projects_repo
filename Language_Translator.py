# import streamlit as st
# from googletrans import Translator, LANGUAGES
# import ssl
# # Fix SSL issues
# ssl._create_default_https_context = ssl._create_unverified_context
# # Initialize Translator
# translator = Translator()
# # Streamlit App Setup
# st.set_page_config(page_title="Language Translator", page_icon="🌎")
# st.write("### 🌎 Language Translator")
# # 📝 Manual Text Input
# text_to_translate = st.text_area("Enter Text to Translate", height=100)
# # 🔄 Language Selection
# language_names = list(LANGUAGES.values())  # Get language names
# language_codes = {v: k for k, v in LANGUAGES.items()}  # Map names to codes
# source_lang_name = st.selectbox("🔄 Source Language", ["Auto Detect"] + language_names)
# target_lang_name = st.selectbox("🎯 Target Language", language_names, index=language_names.index("english"))
# # Convert Language Names to Codes
# source_lang = "auto" if source_lang_name == "Auto Detect" else language_codes[source_lang_name]
# target_lang = language_codes[target_lang_name]
# # 🔁 Translation & Transliteration
# if st.button("Translate", type="primary"):
#     if text_to_translate.strip():
#         try:
#             # ✅ Perfect Translation & Transliteration
#             translated = translator.translate(text_to_translate, src=source_lang, dest=target_lang)
#             st.success("✅ Translation:")
#             st.write(translated.text)  # Proper translation
            
#             # Transliteration (if available)
#             if translated.pronunciation:
#                 st.info(f"🔠 Transliteration: {translated.pronunciation}")
#         except Exception as e:
#             st.error(f"Translation failed: {e}")
#     else:
#         st.warning("⚠️ Please enter text.")

import streamlit as st
import requests
import json
# 🎯 Microsoft Translator API Configuration (Replace with your Azure credentials)
AZURE_API_KEY = "7Inp3S2mze7F2wxqUQB1Soe6brlFPB2an6soiFCQdjDX92wOzukgJQQJ99BCAC3pKaRXJ3w3AAAbACOG8b20"
AZURE_REGION = "eastasia"
AZURE_ENDPOINT = "https://api.cognitive.microsofttranslator.com/"
# 📌 Streamlit App Setup
st.set_page_config(page_title="Microsoft Translator & Transliterator", page_icon="🌍")
st.write("### 🌍 Language Translator")
# 🔄 List of Microsoft Azure Supported Languages
languages = {
    "Auto Detect": "auto",
    "Afrikaans": "af",
    "Arabic": "ar",
    "Bengali": "bn",
    "Chinese Simplified": "zh-Hans",
    "Chinese Traditional": "zh-Hant",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Filipino": "fil",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Korean": "ko",
    "Malay": "ms",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Norwegian": "nb",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Sinhala": "si",
    "Slovak": "sk",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Yoruba": "yo",
    "Zulu": "zu",
}
# 📝 User Input
text_to_translate = st.text_area("Enter text to translate", height=100)
# 🔄 Select Languages
source_lang_name = st.selectbox("🔄 Source Language", list(languages.keys()))
target_lang_name = st.selectbox("🎯 Target Language", list(languages.keys()), index=1)
# Convert Names to Codes
source_lang = "auto" if source_lang_name == "Auto Detect" else languages[source_lang_name]
target_lang = languages[target_lang_name]
# 🔁 Translation & Transliteration Function
def translate_text(text, source_lang, target_lang):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_REGION,
        "Content-Type": "application/json"
    }
    params = {
        "api-version": "3.0",
        "from": source_lang if source_lang != "auto" else None,  # Use auto-detection
        "to": target_lang,
        "toScript": "latn"  # Enables transliteration when available
    }
    body = [{"text": text}]
    
    response = requests.post(AZURE_ENDPOINT, headers=headers, params=params, json=body)
    result = response.json()
    try:
        translation = result[0]["translations"][0]["text"]
        transliteration = result[0]["translations"][0].get("transliteration", {}).get("text", None)
        return translation, transliteration
    except:
        return "⚠️ Translation Error", None
# 🚀 Perform Translation & Transliteration
if st.button("Translate", type="primary"):
    if text_to_translate.strip():
        translated_text, transliterated_text = translate_text(text_to_translate, source_lang, target_lang)
        st.success("✅ Translated Text:")
        st.write(translated_text)
        if transliterated_text:
            st.info(f"🔠 Transliteration: {transliterated_text}")
    else:
        st.warning("⚠️ Please enter text to translate.")
