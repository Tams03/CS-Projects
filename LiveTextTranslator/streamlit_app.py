import streamlit as st
import asyncio
import json
import websockets

st.set_page_config(page_title="Live Text Translator 🌐", layout="centered")

st.title("🌐 Live Text Translator (LinguaLink)")
st.markdown("Chat in different languages — messages are translated instantly!")

# Sidebar
st.sidebar.header("🌎 Choose Languages")
language_map = {
    "English": "en",
    "Hebrew": "he",
    "Spanish": "es",
    "Arabic": "ar",
    "Russian": "ru",
    "French": "fr"
}

user_lang = st.sidebar.selectbox("Your Language", list(language_map.keys()), index=0)
partner_lang = st.sidebar.selectbox("Partner Language", list(language_map.keys()), index=1)

# Backend WebSocket URL (for local or deployed FastAPI backend)
BACKEND_URL = "ws://localhost:8000/ws"  # replace with deployed backend URL if needed

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat box
chat_placeholder = st.empty()

def render_chat():
    with chat_placeholder.container():
        for msg in st.session_state.messages:
            if msg["from"] == "you":
                st.chat_message("user").markdown(msg["text"])
            else:
                st.chat_message("assistant").markdown(f"**Translated:** {msg['text']}")

render_chat()

# User input
user_input = st.chat_input("Type your message...")

async def chat():
    async with websockets.connect(BACKEND_URL) as ws:
        # Send initial language data
        await ws.send(json.dumps({"lang": language_map[user_lang]}))
        # Start a receive loop
        async def receive():
            while True:
                try:
                    data = await ws.recv()
                    msg = json.loads(data)
                    if "message" in msg:
                        st.session_state.messages.append({"from": "partner", "text": msg["message"]})
                        render_chat()
                except Exception:
                    break
        asyncio.create_task(receive())

        # If user sends a message
        if user_input:
            st.session_state.messages.append({"from": "you", "text": user_input})
            render_chat()
            await ws.send(json.dumps({"message": user_input}))

if st.button("🔗 Connect & Start Chat"):
    asyncio.run(chat())
