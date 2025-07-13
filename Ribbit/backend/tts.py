# backend/tts.py

import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sarvamai import SarvamAI

app = FastAPI(title="SarvamAI TTS Service")

# Initialize your SarvamAI client once
client = SarvamAI(
    api_subscription_key="sk_g31vla7l_WnaUHtGA0SuWI397h7yQocQ0",
)

class TTSRequest(BaseModel):
    text: str
    language: str  # e.g. "hi-IN", "en-IN", etc.

@app.post("/synthesize/")
def synthesize(req: TTSRequest):
    """
    Accepts JSON { text, language } and returns:
      { tts_audio_base64: "<base64‑wav>" }
    """
    try:
        # send to SarvamAI
        raw_audio = client.text_to_speech.convert(
            text=req.text,
            target_language_code=req.language,
        )
        if not isinstance(raw_audio, (bytes, bytearray)):
            raise ValueError("Unexpected audio type from SarvamAI")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {e}")

    # Base64‑encode for easy JSON transport
    b64 = base64.b64encode(raw_audio).decode("utf-8")
    return {"tts_audio_base64": b64}
