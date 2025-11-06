# streamlit_app.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

st.set_page_config(page_title="🌐 Live Text Translator Demo", layout="wide")

st.markdown(
    "<h1 style='color:green;'>🌐 Live Text Translator Demo</h1>"
    "<p style='color:green;'>Interactive dual-language chat demo</p>",
    unsafe_allow_html=True
)

st.sidebar.header("Settings")
source_lang = st.sidebar.selectbox("Your Language", ["English", "Spanish", "French", "Hebrew"])
target_lang = st.sidebar.selectbox("Partner Language", ["English", "Spanish", "French", "Hebrew"])

if source_lang == target_lang:
    st.sidebar.warning("Source and target languages are the same!")

# --------------------------
# Translation Setup
# --------------------------
# Map language pairs to small Helsinki-NLP models
model_map = {
    ("English", "Spanish"): "Helsinki-NLP/opus-mt-en-es",
    ("Spanish", "English"): "Helsinki-NLP/opus-mt-es-en",
    ("English", "French"): "Helsinki-NLP/opus-mt-en-fr",
    ("French", "English"): "Helsinki-NLP/opus-mt-fr-en",
    ("English", "Hebrew"): "Helsinki-NLP/opus-mt-en-he",
    ("Hebrew", "English"): "Helsinki-NLP/opus-mt-he-en",
    ("Spanish", "French"): "Helsinki-NLP/opus-mt-es-fr",
    ("French", "Spanish"): "Helsinki-NLP/opus-mt-fr-es",
}

# Cache loaded models
loaded_models = {}

def translate_text(text, src, tgt):
    if src == tgt:
        return text
    key = (src, tgt)
    if key not in loaded_models:
        model_name = model_map.get(key)
        if not model_name:
            return "[Unsupported language pair]"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        loaded_models[key] = (tokenizer, model)
    tokenizer, model = loaded_models[key]
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = model.generate(**inputs, max_length=200)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

# --------------------------
# Chat Interface
# --------------------------
st.subheader("Dual-Language Chat")

if "chat" not in st.session_state:
    st.session_state.chat = []

def send_message():
    msg = st.session_state.input_msg.strip()
    if msg:
        # Your message
        st.session_state.chat.append(f"[You ({source_lang})]: {msg}")
        # Translated message
        translated = translate_text(msg, source_lang, target_lang)
        st.session_state.chat.append(f"[Partner ({target_lang})]: {translated}")
        st.session_state.input_msg = ""

# Chat display
chat_box = st.empty()
with chat_box.container():
    for m in st.session_state.chat:
        if target_lang == "Hebrew" and ("Partner" in m or "You" in m):
            st.markdown(f"<div style='direction:rtl; color:green;'>{m}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)

# Message input
st.text_input("Type a message", key="input_msg", on_change=send_message)
