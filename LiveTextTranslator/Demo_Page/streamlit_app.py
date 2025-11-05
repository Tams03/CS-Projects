import streamlit as st
from deep_translator import GoogleTranslator

# --- Page Config ---
st.set_page_config(page_title="Live Text Translator", layout="wide")

# --- Custom CSS for styling ---
st.markdown("""
    <style>
        body {
            background-color: #a8d5ba;  /* green background */
            color: black;  /* black text */
        }
        .stTextInput>div>div>input {
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

# --- App Title ---
st.title("🌎 Live Text Translator")

# --- Language Selection ---
lang_a = st.selectbox("Chat Area A Language", ["English", "Hebrew"], index=0)
lang_b = st.selectbox("Chat Area B Language", ["English", "Hebrew"], index=1)

language_map = {"English": "en", "Hebrew": "he"}

# --- Chat Areas ---
msg_a = st.text_input("Chat Area A (Type here A → B)")

if st.button("Translate"):
    try:
        translated_text = GoogleTranslator(
            source=language_map[lang_a],
            target=language_map[lang_b]
        ).translate(msg_a)

        # Display messages
        st.markdown(f'<div class="chat-box"><b>{lang_a}:</b> {msg_a}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-box"><b>{lang_b}:</b> {translated_text}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Translation failed: {e}")
