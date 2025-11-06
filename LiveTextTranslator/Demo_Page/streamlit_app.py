# streamlit_app.py
import streamlit as st
from googletrans import Translator

st.set_page_config(page_title="🌐 Live Text Translator Demo", layout="wide")

st.markdown(
    "<h1 style='color:green;'>🌐 Live Text Translator Demo</h1>"
    "<p style='color:green;'>Interactive dual-language chat demo</p>",
    unsafe_allow_html=True
)

# --------------------------
# Sidebar settings
# --------------------------
st.sidebar.header("Settings")
languages = ["English", "Spanish", "French", "Hebrew"]

source_lang = st.sidebar.selectbox("Your Language", languages)
target_lang = st.sidebar.selectbox("Partner Language", languages)

if source_lang == target_lang:
    st.sidebar.warning("Source and target languages are the same!")

# --------------------------
# Translator
# --------------------------
translator = Translator()

def translate_text(text, src, tgt):
    if src == tgt:
        return text
    try:
        translated = translator.translate(text, src=src.lower(), dest=tgt.lower())
        return translated.text
    except Exception:
        return "[Translation failed]"

# --------------------------
# Chat Interface
# --------------------------
st.subheader("Dual-Language Chat")

if "chat" not in st.session_state:
    st.session_state.chat = []

def send_message():
    msg = st.session_state.input_msg.strip()
    if msg:
        # User message
        st.session_state.chat.append(f"[You ({source_lang})]: {msg}")
        # Translated message
        translated = translate_text(msg, source_lang, target_lang)
        st.session_state.chat.append(f"[Partner ({target_lang})]: {translated}")
        st.session_state.input_msg = ""

# Display chat
chat_box = st.container()
with chat_box:
    for m in st.session_state.chat:
        if target_lang == "Hebrew" and ("Partner" in m or "You" in m):
            st.markdown(f"<div style='direction:rtl; color:green;'>{m}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)

# Message input
st.text_input("Type a message", key="input_msg", on_change=send_message)
