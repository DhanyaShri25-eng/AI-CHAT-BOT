from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, Response
from backend.app.services.voice_service import transcribe_audio_file
from backend.app.schemas.all_schemas import VoiceTranscribeResponse, VoiceSpeakRequest

router = APIRouter(prefix="/voice", tags=["Voice"])

@router.post("/transcribe", response_model=VoiceTranscribeResponse)
async def transcribe_voice(
    file: UploadFile = File(...)
):
    """
    Transcribe audio recorded from microphone with multilingual Tamil/English/Tanglish detection
    and extraction of building construction parameters.
    """
    audio_content = await file.read()
    result = transcribe_audio_file(audio_bytes=audio_content, filename=file.filename or "audio.webm")
    return result

@router.post("/speak")
async def text_to_speech(
    payload: VoiceSpeakRequest
):
    """
    TTS endpoint returning speech metadata or synthesizing audio for browser playback.
    """
    return {
        "text": payload.text,
        "language": payload.language,
        "voice_speed": payload.voice_speed,
        "format": "browser-speech-api",
        "status": "ready"
    }
