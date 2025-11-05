import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# --- Page Setup ---
st.set_page_config(page_title="Live Text Translator 🌐", layout="wide")

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

# --- Sidebar: only English ↔ Hebrew ---
st.sidebar.header("🌎 Choose Languages")
language_map = {"English": "en", "Hebrew": "he"}
lang_a = st.sidebar.selectbox("Chat Area A Language", list(language_map.keys()), index=0)
lang_b = st.sidebar.selectbox("Chat Area B Language", list(language_map.keys()), index=1)

# --- Load translation model ---
@st.cache_resource
def load_translator():
    st.info("Loading translation model for English ↔ Hebrew...")
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-he")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-he")
    translator = pipeline("translation", model=model, tokenizer=tokenizer)
    st.success("Model loaded successfully!")
    return translator

translator = load_translator()

# --- Translation function ---
def translate_text(text, source_lang, target_lang):
    if source_lang == "en" and target_lang == "he":
        result = translator(text, src="en", tgt="he")
        return result[0]['translation_text']
    elif source_lang == "he" and target_lang == "en":
        result = translator(text, src="he", tgt="en")
        return result[0]['translation_text']
    else:
        return "[Unsupported language]"

# --- Chat state ---
if "chat_a" not in st.session_state:
    st.session_state.chat_a = []
if "chat_b" not in st.session_state:
    st.session_state.chat_b = []

if "input_a_val" not in st.session_state:
    st.session_state.input_a_val = ""
if "input_b_val" not in st.session_state:
    st.session_state.input_b_val = ""

# --- Layout: dual chat columns ---
col1, col2 = st.columns(2)

# --- Chat Area A ---
with col1:
    st.subheader(f"Chat Area A ({lang_a})")
    for msg in st.session_state.chat_a:
        st.markdown(f"<div class='chat-box'>{msg}</div>", unsafe_allow_html=True)

    msg_a = st.text_input(
        "Type here (A → B)",
        key="input_a_widget",
        value=st.session_state.input_a_val,
    )

    if st.button("Send from A", key="send_a") and msg_a.strip():
        translated = translate_text(msg_a, language_map[lang_a], language_map[lang_b])
        st.session_state.chat_a.append(f"**You ({lang_a}):** {msg_a}")
        st.session_state.chat_b.append(f"**Translated to {lang_b}:** {translated}")
        st.session_state.input_a_val = ""  # reset safely

# --- Chat Area B ---
with col2:
    st.subheader(f"Chat Area B ({lang_b})")
    for msg in st.session_state.chat_b:
        st.markdown(f"<div class='chat-box'>{msg}</div>", unsafe_allow_html=True)

    msg_b = st.text_input(
        "Type here (B → A)",
        key="input_b_widget",
        value=st.session_state.input_b_val,
    )

    if st.button("Send from B", key="send_b") and msg_b.strip():
        translated = translate_text(msg_b, language_map[lang_b], language_map[lang_a])
        st.session_state.chat_b.append(f"**You ({lang_b}):** {msg_b}")
        st.session_state.chat_a.append(f"**Translated to {lang_a}:** {translated}")
        st.session_state.input_b_val = ""  # reset safely
