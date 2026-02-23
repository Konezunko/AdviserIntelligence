import base64
import io
from gtts import gTTS

def generate_audio(text: str) -> str:
    """
    Generates audio from text using gTTS and returns it as a base64 encoded string.
    """
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang='ja')
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_content = mp3_fp.read()
        return base64.b64encode(audio_content).decode('utf-8')
    except Exception as e:
        print(f"Error generating audio: {e}")
        return ""

def create_slides(context: str) -> list[dict]:
    """
    Generates a list of slides based on the context.
    For this PoC, it returns a placeholder slide with the context summary or title.
    Real implementation would analyze context to pick specific PDF pages.
    """
    # specific logic to parse context and find relevant page numbers or images could go here.
    # For PoC, we return a generic slide structure.
    return [
        {
            "type": "title",
            "text": "解説",
            "image": None # Placeholder for URL
        }
    ]
