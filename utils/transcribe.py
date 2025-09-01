import os
import openai
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

# Usar la API key desde .env
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY no encontrada en .env")

def transcribe_audio(audio_path):
    try:
        print(f"[DEBUG] Transcribiendo audio: {audio_path}")
        with open(audio_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
        # Usar .text en lugar de ['text']
        print(f"[DEBUG] Transcripción recibida (primeros 200 chars): {transcript.text[:200]}...")
        return transcript.text
    except openai.error.OpenAIError as e:
        print(f"[ERROR] Error transcribiendo audio: {e}")
        raise
