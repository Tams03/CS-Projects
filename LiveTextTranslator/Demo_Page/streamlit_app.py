import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="🌐 Dual-Language Chat Demo", layout="wide")

st.markdown(
    "<h1 style='color:green;'>🌐 Dual-Language Chat Demo</h1>"
    "<p style='color:green;'>Type in either box to see the translation appear in the other box</p>",
    unsafe_allow_html=True
)

languages = ["English", "Spanish", "French", "Hebrew"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("User A")
    src_lang_a = st.selectbox("Language A", languages, key="src_a")
    tgt_lang_a = st.selectbox("Translate to Language B", languages, index=1, key="tgt_a")
    
with col2:
    st.subheader("User B")
    src_lang_b = st.selectbox("Language B", languages, key="src_b")
    tgt_lang_b = st.selectbox("Translate to Language A", languages, index=0, key="tgt_b")

if "chat_a" not in st.session_state:
    st.session_state.chat_a = []
if "chat_b" not in st.session_state:
    st.session_state.chat_b = []

# --------------------------
# Translator
# --------------------------
def translate(text, src, tgt):
    if src == tgt:
        return text
    try:
        return GoogleTranslator(source=src.lower(), target=tgt.lower()).translate(text)
    except:
        return "[Translation failed]"

# --------------------------
# Input boxes
# --------------------------
with col1:
    msg_a = st.text_input("Type message as User A", key="input_a")
    if st.button("Send A → B", key="btn_a") and msg_a.strip():
        translated = translate(msg_a, src_lang_a, tgt_lang_a)
        st.session_state.chat_b.append(f"[User A]: {translated}")
        # Clear input after sending
        st.experimental_rerun()

with col2:
    msg_b = st.text_input("Type message as User B", key="input_b")
    if st.button("Send B → A", key="btn_b") and msg_b.strip():
        translated = translate(msg_b, src_lang_b, tgt_lang_b)
        st.session_state.chat_a.append(f"[User B]: {translated}")
        # Clear input after sending
        st.experimental_rerun()

# --------------------------
# Display chats
# --------------------------
with col1:
    st.subheader("Messages received by A")
    for m in st.session_state.chat_a:
        if tgt_lang_b == "Hebrew":
            st.markdown(f"<div style='direction:rtl; color:green;'>{m}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("Messages received by B")
    for m in st.session_state.chat_b:
        if tgt_lang_a == "Hebrew":
            st.markdown(f"<div style='direction:rtl; color:green;'>{m}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:green;'>{m}</div>", unsafe_allow_html=True)
