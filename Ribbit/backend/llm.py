# backend/llm.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Gemini Flash LLM Service")

API_KEY    = "AIzaSyD_0j1_XqS3U4lPtHj25eSSRR0NBp6irsc"
MODEL_PATH = "models/gemini-2.0-flash:generateContent"
URL        = f"https://generativelanguage.googleapis.com/v1beta2/{MODEL_PATH}?key={API_KEY}"

class LLMRequest(BaseModel):
    prompt: str

@app.post("/llm/")
def generate(request: LLMRequest):
    """
    Sends the user prompt to Gemini Flash and returns the generated text.
    """
    payload = { "prompt": { "text": request.prompt } }
    resp = requests.post(URL, json=payload)
    if not resp.ok:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    try:
        output = data["candidates"][0]["output"].strip()
    except (KeyError, IndexError):
        raise HTTPException(status_code=502, detail="Unexpected LLM response format")
    return {"response": output}
