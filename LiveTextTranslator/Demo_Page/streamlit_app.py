import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Page Setup ---
st.set_page_config(page_title="LinguaLink 🌐", page_icon="💬", layout="wide")

# --- Green Theme Styling ---
st.markdown("""
    <style>
        body { background-color: #f5fff5; }
        .stApp { background-color: #f5fff5; }
        h1, h2, h3, h4, h5, h6, label, p { color: #006400 !important; }
        div[data-testid="stSidebar"] { background-color: #e6f7e6; }
        div.stButton > button {
            background-color: #2e8b57 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
        }
        div.stButton > button:hover {
            background-color: #3cb371 !important;
            color: white !important;
        }
        hr { border: 1px solid #9acd32; }
        .chat-bubble {
            border-radius: 12px;
            padding: 8px 12px;
            margin: 5px 0;
            max-width: 80%;
        }
        .speakerA { background-color: #d9fdd3; align-self: flex-start; }
        .speakerB { background-color: #e6e6e6; align-self: flex-end; }
        .translation { font-size: 0.9em; color: #006400; margin-top: 3px; }
    </style>
""", unsafe_allow_html=True)

# --- Title Section ---
st.markdown("<h1 style='text-align:center;'>💬 LinguaLink — Live Multilingual Chat</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#006400;'>Try a face-to-face bilingual conversation in real time, powered by Meta’s NLLB model.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Load Model (cached) ---
@st.cache_resource
def load_model():
    model_name = "facebook/nllb-200-distilled-1.3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# --- Supported Languages ---
language_codes = {
    "English": "eng_Latn",
    "Hebrew": "heb_Hebr",
    "Spanish": "spa_Latn",
    "Arabic": "arb_Arab",
    "Russian": "rus_Cyrl",
    "French": "fra_Latn"
}

# --- Translation Function ---
def translate_text(text, target_lang):
    try:
        tgt_code = language_codes[target_lang]
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=200)
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_code),
            max_length=200
        )
        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    except Exception as e:
        return f"[Translation failed: {e}]"

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Conversation Settings")
speaker_a_lang = st.sidebar.selectbox("👤 Speaker A Language", list(language_codes.keys()), index=0)
speaker_b_lang = st.sidebar.selectbox("👤 Speaker B Language", list(language_codes.keys()), index=1)
st.sidebar.markdown("---")
st.sidebar.markdown("💡 *Tip:* Choose two different languages to simulate a live bilingual chat!")

# --- Initialize chat history ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# --- Chat Input Area ---
col1, col2 = st.columns(2)

with col1:
    a_message = st.text_input(f"🗣️ Speaker A ({speaker_a_lang})", key="a_input")
    if st.button("Send as A 💬"):
        if a_message.strip():
            translated = translate_text(a_message, speaker_b_lang)
            st.session_state.conversation.append(
                {"speaker": "A", "lang": speaker_a_lang, "message": a_message, "translated": translated, "target_lang": speaker_b_lang}
            )

with col2:
    b_message = st.text_input(f"🗣️ Speaker B ({speaker_b_lang})", key="b_input")
    if st.button("Send as B 💬"):
        if b_message.strip():
            translated = translate_text(b_message, speaker_a_lang)
            st.session_state.conversation.append(
                {"speaker": "B", "lang": speaker_b_lang, "message": b_message, "translated": translated, "target_lang": speaker_a_lang}
            )

st.markdown("---")

# --- Display Conversation ---
st.subheader("🗨️ Conversation History")
chat_container = st.container()

for msg in reversed(st.session_state.conversation):
    if msg["speaker"] == "A":
        st.markdown(f"""
        <div class="chat-bubble speakerA">
            <b>👤 A ({msg['lang']}):</b> {msg['message']}
            <div class="translation">🌐 → {msg['target_lang']}: {msg['translated']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-bubble speakerB" style="margin-left:auto;">
            <b>👤 B ({msg['lang']}):</b> {msg['message']}
            <div class="translation">🌐 → {msg['target_lang']}: {msg['translated']}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>🌿 Powered by Meta NLLB-200 & Streamlit | Built with 💚 by Tami Lieberman</p>", unsafe_allow_html=True)
