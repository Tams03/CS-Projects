import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

st.set_page_config(page_title="Live Text Translator 🌐", layout="wide")
st.markdown(
    "<h1 style='color:green;'>🌐 Live Text Translator (LinguaLink)</h1>"
    "<p style='color:green;'>Simulate a bilingual conversation — type in either chat and see the translation instantly!</p>",
    unsafe_allow_html=True
)

# Load model once
@st.cache_resource
def load_model():
    print("[INFO] Loading translation model...")
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("[INFO] Model loaded successfully.")
    return tokenizer, model

tokenizer, model = load_model()

LANGUAGE_CODES = {
    "English": "eng_Latn",
    "Hebrew": "heb_Hebr",
    "Spanish": "spa_Latn",
    "Arabic": "arb_Arab",
    "Russian": "rus_Cyrl",
    "French": "fra_Latn"
}

def translate(text, source, target):
    if source == target:
        return text
    tokenizer.src_lang = LANGUAGE_CODES[source]
    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.lang_code_to_id[LANGUAGE_CODES[target]],
        max_length=200
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

# --- Dual chat interface ---
col1, col2 = st.columns(2)

if "chat_A" not in st.session_state:
    st.session_state.chat_A = []
if "chat_B" not in st.session_state:
    st.session_state.chat_B = []

# Chat A
with col1:
    st.subheader("Chat A")
    lang_A = st.selectbox("Language", list(LANGUAGE_CODES.keys()), key="lang_A")
    msg_A = st.text_input("Type a message...", key="input_A")
    if st.button("Send from A → B", key="send_A"):
        if msg_A.strip():
            translated = translate(msg_A, lang_A, st.session_state.lang_B)
            st.session_state.chat_A.append(f"You ({lang_A}): {msg_A}")
            st.session_state.chat_B.append(f"Translated ({st.session_state.lang_B}): {translated}")

    st.markdown("**Conversation:**")
    for m in st.session_state.chat_A:
        st.markdown(m)

# Chat B
with col2:
    st.subheader("Chat B")
    lang_B = st.selectbox("Language", list(LANGUAGE_CODES.keys()), key="lang_B")
    msg_B = st.text_input("Type a message...", key="input_B")
    if st.button("Send from B → A", key="send_B"):
        if msg_B.strip():
            translated = translate(msg_B, lang_B, st.session_state.lang_A)
            st.session_state.chat_B.append(f"You ({lang_B}): {msg_B}")
            st.session_state.chat_A.append(f"Translated ({st.session_state.lang_A}): {translated}")

    st.markdown("**Conversation:**")
    for m in st.session_state.chat_B:
        st.markdown(m)
