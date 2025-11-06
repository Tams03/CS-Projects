import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="🌐 Dual-Language Chat Demo", layout="wide")

languages = ["English", "Hebrew"]

# Initialize session state
for key in ["chat_a", "chat_b"]:
    if key not in st.session_state:
        st.session_state[key] = []

# Translator function
def translate(text, src, tgt):
    if not text.strip() or src == tgt:
        return text
    try:
        return GoogleTranslator(source=src.lower(), target=tgt.lower()).translate(text)
    except:
        return "[Translation failed]"

col1, col2 = st.columns(2)

with col1:
    st.subheader("User A")
    lang_a = st.selectbox("Language A", languages, key="src_a")
    lang_b = st.selectbox("Translate to Language B", languages, index=1, key="tgt_a")
    
    # Input box with callback
    def send_a():
        translated = translate(st.session_state.input_a, lang_a, lang_b)
        st.session_state.chat_b.append(translated)
        st.session_state.input_a = ""  # clear input safely via callback

    st.text_input("Type message as User A", key="input_a", on_change=send_a)

    st.subheader("Messages received by A")
    for m in st.session_state.chat_a:
        st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("User B")
    lang_b_src = st.selectbox("Language B", languages, key="src_b")
    lang_a_tgt = st.selectbox("Translate to Language A", languages, index=0, key="tgt_b")

    def send_b():
        translated = translate(st.session_state.input_b, lang_b_src, lang_a_tgt)
        st.session_state.chat_a.append(translated)
        st.session_state.input_b = ""

    st.text_input("Type message as User B", key="input_b", on_change=send_b)

    st.subheader("Messages received by B")
    for m in st.session_state.chat_b:
        st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)
