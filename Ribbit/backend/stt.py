# backend/stt.py

from fastapi import FastAPI, UploadFile, File, HTTPException
import soundfile as sf
import io
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment

app = FastAPI(title="Whisper STT Service")

# Load models once at startup
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.config.forced_decoder_ids = None


def convert_to_wav(raw_bytes: bytes, fmt: str) -> bytes:
    """
    Convert various audio formats to WAV using pydub for compatibility with soundfile.
    """
    try:
        # pydub expects format strings like 'webm', 'mp3', etc.
        audio = AudioSegment.from_file(io.BytesIO(raw_bytes), format=fmt)
        wav_io = io.BytesIO()
        audio.export(wav_io, format='wav')
        return wav_io.getvalue()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Audio conversion failed: {e}")


@app.post("/stt/")
async def transcribe(audio: UploadFile = File(...)):
    """
    Accepts a user-uploaded audio file, converts to WAV if needed, runs Whisper-tiny,
    and returns the transcription.
    """
    try:
        raw = await audio.read()
        content_type = audio.content_type or ''
        # Determine format for pydub (e.g. 'webm', 'mp3')
        if content_type.startswith('audio/') and not content_type.endswith('/wav'):
            fmt = content_type.split('/')[-1]
            wav_bytes = convert_to_wav(raw, fmt)
        else:
            wav_bytes = raw
        data, samplerate = sf.read(io.BytesIO(wav_bytes), dtype='float32')
    except HTTPException:
        # propagate conversion errors
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read audio: {e}")

    # Prepare input for Whisper
    inputs = processor(data, sampling_rate=samplerate, return_tensors="pt").input_features
    predicted_ids = model.generate(inputs)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()
    return {"transcription": transcription}
