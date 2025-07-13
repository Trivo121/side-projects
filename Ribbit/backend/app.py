# backend/app.py

import io
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import soundfile as sf
import requests

# transformers / Whisper
from transformers import WhisperProcessor, WhisperForConditionalGeneration

# our new SarvamAI TTS wrapper
from tts import synthesize as sarvam_synthesize


app = FastAPI(title="Ribbit Voice Assistant API")

# — Allow CORS from React dev server —  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# —— CONFIG ——  
API_KEY    = "AIzaSyD_0j1_XqS3U4lPtHj25eSSRR0NBp6irsc"
MODEL_PATH = "models/gemini-2.0-flash:generateContent"
LLM_URL    = f"https://generativelanguage.googleapis.com/v1beta2/{MODEL_PATH}?key={API_KEY}"

# —— LOAD MODELS ONCE ——  
whisper_proc  = WhisperProcessor.from_pretrained("openai/whisper-tiny")
whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
whisper_model.config.forced_decoder_ids = None

# —— HELPERS ——  
def whisper_transcribe(wav_bytes: bytes) -> str:
    data, sr = sf.read(io.BytesIO(wav_bytes))
    features = whisper_proc(data, sampling_rate=sr, return_tensors="pt").input_features
    ids       = whisper_model.generate(features)
    return whisper_proc.batch_decode(ids, skip_special_tokens=True)[0].strip()

def call_gemini(prompt: str) -> str:
    payload = {"prompt": {"text": prompt}}
    r = requests.post(LLM_URL, json=payload)
    if not r.ok:
        raise HTTPException(status_code=502, detail=r.text)
    js = r.json()
    try:
        return js["candidates"][0]["output"].strip()
    except Exception:
        raise HTTPException(status_code=502, detail="Unexpected LLM response")

class TextPayload(BaseModel):
    text: str
    language: str

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/languages")
def languages():
    return {
        "languages": [
            { "code": "hi-IN", "name": "Hindi"    },
            { "code": "bn-IN", "name": "Bengali"  },
            { "code": "ta-IN", "name": "Tamil"    },
            { "code": "te-IN", "name": "Telugu"   },
            { "code": "gu-IN", "name": "Gujarati" },
            { "code": "kn-IN", "name": "Kannada"  },
            { "code": "ml-IN", "name": "Malayalam"},
            { "code": "mr-IN", "name": "Marathi"  },
            { "code": "pa-IN", "name": "Punjabi"  },
            { "code": "od-IN", "name": "Odia"     },
            { "code": "en-IN", "name": "English"  }
        ]
    }

@app.post("/process-text")
def process_text(payload: TextPayload):
    """
    JSON { text, language } → Gemini → SarvamAI TTS
    """
    llm_resp = call_gemini(payload.text)

    # delegate to tts.py
    tts_resp = sarvam_synthesize({"text": llm_resp, "language": payload.language})
    return {
        "llm_response": llm_resp,
        "tts_audio_base64": tts_resp["tts_audio_base64"]
    }

@app.post("/process-voice")
async def process_voice(
    audio: UploadFile = File(...),
    language: str      = Form(...)
):
    """
    Multipart form:
      - audio: WAV/WEBM blob
      - language: "en-IN", etc.
    → Whisper STT → Gemini → SarvamAI TTS
    """
    raw = await audio.read()
    try:
        transcription = whisper_transcribe(raw)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"STT failed: {e}")

    llm_resp = call_gemini(transcription)

    try:
        tts_resp = sarvam_synthesize({"text": llm_resp, "language": language})
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")

    return JSONResponse({
        "transcription": transcription,
        "llm_response": llm_resp,
        "tts_audio_base64": tts_resp["tts_audio_base64"]
    })
