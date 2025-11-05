from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Your original translation code ---
print("[INFO] Loading translation model...")
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
print("[INFO] Model loaded successfully.")

LANGUAGE_CODES = {
    "en": "eng_Latn",
    "he": "heb_Hebr",
    "es": "spa_Latn",
    "ar": "arb_Arab",
    "ru": "rus_Cyrl",
    "fr": "fra_Latn"
}

def translate_text(text, source_lang, target_lang):
    if source_lang not in LANGUAGE_CODES or target_lang not in LANGUAGE_CODES:
        return "[Unsupported language]"
    tokenizer.src_lang = LANGUAGE_CODES[source_lang]
    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.lang_code_to_id[LANGUAGE_CODES[target_lang]],
        max_length=200
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

# --- FastAPI app ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Request model ---
class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

# --- API endpoint for demo ---
@app.post("/translate")
def translate(req: TranslationRequest):
    translated = translate_text(req.text, req.source_lang, req.target_lang)
    return {"translated_text": translated}

# Run with: uvicorn backend:app --host 0.0.0.0 --port 8000
