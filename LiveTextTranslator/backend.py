import threading
import time
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from websocket import create_connection

# Load translation model (NLLB for multilingual support)
print("[INFO] Loading translation model...")
model_name = "facebook/nllb-200-distilled-600M"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("[INFO] Model loaded successfully.")
except Exception as e:
    print(f"[ERROR] Model load failed: {e}")
    exit(1)

# NLLB language codes
language_codes = {
    "en": "eng_Latn",
    "he": "heb_Hebr",
    "es": "spa_Latn",
    "ar": "arb_Arab",
    "ru": "rus_Cyrl",
    "fr": "fra_Latn"
}

# Translation function
def translate_text(text, source_lang, target_lang):
    try:
        if source_lang not in language_codes or target_lang not in language_codes:
            return "[Unsupported language]"
        src_code = language_codes[source_lang]
        tgt_code = language_codes[target_lang]
        tokenizer.src_lang = src_code
        encoded = tokenizer(text, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded,
            forced_bos_token_id=tokenizer.lang_code_to_id[tgt_code],
            max_length=200
        )
        return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    except Exception as e:
        print(f"[TRANSLATION ERROR] {e}")
        return "[Translation failed]"

# FastAPI server setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[dict] = []
        self.waiting_connections: list[dict] = []

    async def connect(self, websocket: WebSocket, preferred_lang: str):
        print(f"[DEBUG] New client connection request: {preferred_lang}")
        if preferred_lang not in language_codes:
            await websocket.send_json({"error": "Unsupported language"})
            await websocket.close()
            print(f"[DEBUG] Client disconnected: unsupported language {preferred_lang}")
            return

        connection = {"ws": websocket, "lang": preferred_lang, "paired_with": None}
        self.active_connections.append(connection)
        self.waiting_connections.append(connection)
        print(f"[DEBUG] Active connections: {[c['lang'] for c in self.active_connections]}")
        print(f"[DEBUG] Waiting connections: {[c['lang'] for c in self.waiting_connections]}")

        if len(self.waiting_connections) >= 2:
            conn1 = self.waiting_connections.pop(0)
            conn2 = self.waiting_connections.pop(0)
            conn1["paired_with"] = conn2
            conn2["paired_with"] = conn1
            print(f"[DEBUG] Paired clients: {conn1['lang']} <-> {conn2['lang']}")

    def disconnect(self, websocket: WebSocket):
        connection = next((c for c in self.active_connections if c["ws"] == websocket), None)
        if connection:
            print(f"[DEBUG] Disconnecting client: {connection['lang']}")
            if connection["paired_with"]:
                connection["paired_with"]["paired_with"] = None
            self.active_connections.remove(connection)
            self.waiting_connections = [c for c in self.waiting_connections if c["ws"] != websocket]
            print(f"[DEBUG] Active connections after disconnect: {[c['lang'] for c in self.active_connections]}")

    async def broadcast(self, message: str, sender_ws: WebSocket):
        sender = next(c for c in self.active_connections if c["ws"] == sender_ws)
        print(f"[DEBUG] Message received from {sender['lang']}: {message}")

        if not sender["paired_with"]:
            await sender_ws.send_json({"message": "Waiting for partner..."})
            print(f"[DEBUG] {sender['lang']} is waiting for a partner.")
            return

        receiver = sender["paired_with"]
        translated = translate_text(message, sender['lang'], receiver['lang'])
        print(f"[DEBUG] Translation result: {translated}")
        await receiver["ws"].send_json({"message": translated, "from": sender['lang']})
        print(f"[DEBUG] Sent translated message to {receiver['lang']}")

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        preferred_lang = await websocket.receive_json()
        if not preferred_lang or "lang" not in preferred_lang:
            await websocket.send_json({"error": "Invalid language data"})
            await websocket.close()
            return
        await manager.connect(websocket, preferred_lang["lang"])
        while True:
            data = await websocket.receive_json()
            if not data or "message" not in data:
                await websocket.send_json({"error": "Invalid message data"})
                continue
            await manager.broadcast(data["message"], websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"[ERROR] WebSocket error: {e}")
        manager.disconnect(websocket)

# Run server in thread
def run_server():
    print("[SERVER] Starting WebSocket server on ws://localhost:8000/ws ...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # 0.0.0.0 for Codespaces access

threading.Thread(target=run_server, daemon=True).start()
time.sleep(3)  # Allow server to start
