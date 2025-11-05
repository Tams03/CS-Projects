import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Page Setup ---
st.set_page_config(page_title="Live Text Translator 🌐", layout="wide")
st.markdown(
    "<h1 style='color:green;'>🌐 Live Text Translator (LinguaLink)</h1>"
    "<p style='color:green;'>Simulate a multilingual conversation — type messages in either chat area and see instant translations!</p>",
    unsafe_allow_html=True
)

# --- Sidebar for language selection ---
st.sidebar.header("🌎 Choose Languages")
language_map = {
    "English": "en",
    "Hebrew": "he",
    "Spanish": "es",
    "Arabic": "ar",
    "Russian": "ru",
    "French": "fr"
}

lang_a = st.sidebar.selectbox("Chat Area A Language", list(language_map.keys()), index=0)
lang_b = st.sidebar.selectbox("Chat Area B Language", list(language_map.keys()), index=1)

# --- Chat state ---
if "chat_a" not in st.session_state:
    st.session_state.chat_a = []
if "chat_b" not in st.session_state:
    st.session_state.chat_b = []

# --- Input value state ---
if "input_a_val" not in st.session_state:
    st.session_state.input_a_val = ""
if "input_b_val" not in st.session_state:
    st.session_state.input_b_val = ""

# --- Lazy model loading ---
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.tokenizer = None
    st.session_state.model = None

def load_model():
    try:
        st.info("Loading translation model... This may take a while.")
        model_name = "facebook/nllb-200-distilled-600M"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        st.session_state.tokenizer = tokenizer
        st.session_state.model = model
        st.session_state.model_loaded = True
        st.success("Model loaded successfully!")
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.warning("Using simulated translation for now.")

LANGUAGE_CODES = {
    "en": "eng_Latn",
    "he": "heb_Hebr",
    "es": "spa_Latn",
    "ar": "arb_Arab",
    "ru": "rus_Cyrl",
    "fr": "fra_Latn"
}

def translate_text(text, source_lang, target_lang):
    # fallback if model failed
    if not st.session_state.model_loaded:
        load_model()
        if not st.session_state.model_loaded:
            return f"[Simulated translation of '{text}' from {source_lang} → {target_lang}]"

    tokenizer = st.session_state.tokenizer
    model = st.session_state.model

    if source_lang not in LANGUAGE_CODES or target_lang not in LANGUAGE_CODES:
        return "[Unsupported language]"

    tokenizer.src_lang = LANGUAGE_CODES[source_lang]
    encoded = tokenizer(text, return_tensors="pt")
    if hasattr(tokenizer, "lang_code_to_id"):
        bos_id = tokenizer.lang_code_to_id[LANGUAGE_CODES[target_lang]]
    else:
        bos_id = tokenizer.convert_tokens_to_ids(f"<{LANGUAGE_CODES[target_lang]}>")

    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=bos_id,
        max_length=200
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

# --- Layout: dual chat columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Chat Area A ({lang_a})")
    for msg in st.session_state.chat_a:
        st.markdown(msg)

    msg_a = st.text_input(
        "Type here (A → B)",
        key="input_a_widget",
        value=st.session_state.input_a_val,
    )

    if st.button("Send from A", key="send_a") and msg_a.strip():
        translated = translate_text(msg_a, language_map[lang_a], language_map[lang_b])
        st.session_state.chat_a.append(f"**You ({lang_a}):** {msg_a}")
        st.session_state.chat_b.append(f"**Translated to {lang_b}:** {translated}")
        st.session_state.input_a_val = ""

with col2:
    st.subheader(f"Chat Area B ({lang_b})")
    for msg in st.session_state.chat_b:
        st.markdown(msg)

    msg_b = st.text_input(
        "Type here (B → A)",
        key="input_b_widget",
        value=st.session_state.input_b_val,
    )

    if st.button("Send from B", key="send_b") and msg_b.strip():
        translated = translate_text(msg_b, language_map[lang_b], language_map[lang_a])
        st.session_state.chat_b.append(f"**You ({lang_b}):** {msg_b}")
        st.session_state.chat_a.append(f"**Translated to {lang_a}:** {translated}")
        st.session_state.input_b_val = ""
