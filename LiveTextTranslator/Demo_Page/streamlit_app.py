import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="LinguaLink 🌐 Live Translator",
    layout="wide",
    page_icon="🌐"
)

# Custom CSS for green theme
st.markdown(
    """
    <style>
    .stApp {background-color: #e6f2e6;}
    .stButton>button {background-color: #2e7d32; color: white;}
    .stTextInput>div>div>input {background-color: #f0fff0;}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 style='text-align:center; color:#2e7d32;'>🌐 Live Text Translator (LinguaLink)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Simulate a bilingual chat — type in one language and see it translated in the other!</p>", unsafe_allow_html=True)

# Sidebar: language selection
st.sidebar.header("🌎 Choose Languages")
LANG_MAP = {
    "English": "en",
    "Hebrew": "he",
    "Spanish": "es",
    "Arabic": "ar",
    "Russian": "ru",
    "French": "fr"
}

lang_a_name = st.sidebar.selectbox("Language A", list(LANG_MAP.keys()), index=0)
lang_b_name = st.sidebar.selectbox("Language B", list(LANG_MAP.keys()), index=1)
lang_a = LANG_MAP[lang_a_name]
lang_b = LANG_MAP[lang_b_name]

# Backend URL
BACKEND_URL = "http://localhost:8000/translate"  # replace with deployed backend URL

# Session state for dual chat
if "chat_a" not in st.session_state:
    st.session_state.chat_a = []
if "chat_b" not in st.session_state:
    st.session_state.chat_b = []

# Function to call backend
def translate_text(text, source_lang, target_lang):
    try:
        res = requests.post(BACKEND_URL, json={
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        })
        if res.status_code == 200:
            return res.json().get("translated_text", "[Error]")
        return "[Error]"
    except Exception as e:
        return f"[Error: {e}]"

# Columns for dual chat
col1, col2 = st.columns(2)

# Chat A panel
with col1:
    st.subheader(f"Chat in {lang_a_name}")
    for msg in st.session_state.chat_a:
        st.markdown(msg)
    msg_a = st.text_input(f"Type in {lang_a_name}", key="input_a")
    if st.button(f"Send {lang_a_name} → {lang_b_name}", key="btn_a") and msg_a:
        st.session_state.chat_a.append(f"**You ({lang_a_name}):** {msg_a}")
        translated = translate_text(msg_a, lang_a, lang_b)
        st.session_state.chat_b.append(f"**Translated ({lang_b_name}):** {translated}")
        st.experimental_rerun()

# Chat B panel
with col2:
    st.subheader(f"Chat in {lang_b_name}")
    for msg in st.session_state.chat_b:
        st.markdown(msg)
    msg_b = st.text_input(f"Type in {lang_b_name}", key="input_b")
    if st.button(f"Send {lang_b_name} → {lang_a_name}", key="btn_b") and msg_b:
        st.session_state.chat_b.append(f"**You ({lang_b_name}):** {msg_b}")
        translated = translate_text(msg_b, lang_b, lang_a)
        st.session_state.chat_a.append(f"**Translated ({lang_a_name}):** {translated}")
        st.experimental_rerun()
