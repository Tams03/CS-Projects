import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="🌐 Dual-Language Chat Demo", layout="wide")
st.markdown("<h1 style='color:green;'>🌐 Dual-Language Chat Demo</h1>", unsafe_allow_html=True)

languages = ["English", "Spanish", "French", "Hebrew"]

# Initialize session state
for key in ["input_a", "input_b", "chat_a", "chat_b"]:
    if key not in st.session_state:
        st.session_state[key] = "" if "input" in key else []

col1, col2 = st.columns(2)

# Translator function
def translate(text, src, tgt):
    if src == tgt or not text.strip():
        return text
    try:
        return GoogleTranslator(source=src.lower(), target=tgt.lower()).translate(text)
    except:
        return "[Translation failed]"

with col1:
    st.subheader("User A")
    lang_a = st.selectbox("Language A", languages, key="src_a")
    lang_b = st.selectbox("Translate to Language B", languages, index=1, key="tgt_a")
    msg_a = st.text_area("Type message as User A", st.session_state.input_a, key="input_a")
    if st.button("Send A → B"):
        translated = translate(msg_a, lang_a, lang_b)
        st.session_state.chat_b.append(translated)
        st.session_state.input_a = ""  # Clear input after sending

    st.subheader("Messages received by A")
    for m in st.session_state.chat_a:
        st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("User B")
    lang_b_src = st.selectbox("Language B", languages, key="src_b")
    lang_a_tgt = st.selectbox("Translate to Language A", languages, index=0, key="tgt_b")
    msg_b = st.text_area("Type message as User B", st.session_state.input_b, key="input_b")
    if st.button("Send B → A"):
        translated = translate(msg_b, lang_b_src, lang_a_tgt)
        st.session_state.chat_a.append(translated)
        st.session_state.input_b = ""  # Clear input after sending

    st.subheader("Messages received by B")
    for m in st.session_state.chat_b:
        st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)
