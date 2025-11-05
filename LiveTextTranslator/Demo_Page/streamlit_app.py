# streamlit_app.py
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Live Text Translator 🌎", layout="wide")

st.title("🌎 Live Text Translator")

# --- Custom CSS for styling ---
st.markdown("""
    <style>
        body {
            background-color: #a8d5ba;  /* green background */
            color: black;  /* black text */
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: white;  /* white input boxes */
            color: black;
        }
        .stButton>button {
            background-color: #ffffff;  /* white buttons */
            color: black;
        }
        .chat-box {
            background-color: white;  /* white chat messages */
            padding: 8px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Language Selection ---
languages = ["English", "Hebrew"]

col1, col2 = st.columns(2)
with col1:
    lang_a = st.selectbox("Chat Area A Language", languages, index=0)
with col2:
    lang_b = st.selectbox("Chat Area B Language", languages, index=1)

# --- Load translation pipelines ---
@st.cache_resource
def load_pipelines():
    translator_en_he = pipeline("translation", model="Helsinki-NLP/opus-mt-en-he")
    translator_he_en = pipeline("translation", model="Helsinki-NLP/opus-mt-he-en")
    return translator_en_he, translator_he_en

translator_en_he, translator_he_en = load_pipelines()

# --- Translation function ---
def translate_text(text, source_lang, target_lang):
    if source_lang == "English" and target_lang == "Hebrew":
        result = translator_en_he(text)
    elif source_lang == "Hebrew" and target_lang == "English":
        result = translator_he_en(text)
    else:
        # Same language, no translation needed
        return text
    return result[0]['translation_text']

# --- Chat input ---
st.write("Type your message below:")

msg_a = st.text_area(f"Chat Area A ({lang_a})", height=100, key="msg_a")

if st.button("Translate →"):
    if msg_a.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        translated = translate_text(msg_a, lang_a, lang_b)
        st.text_area(f"Chat Area B ({lang_b})", value=translated, height=100, key="msg_b")

st.write("---")
st.caption("Powered by Hugging Face Transformers (Helsinki-NLP)")
