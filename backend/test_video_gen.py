import sys
import os

# Add app to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.rag import get_video_script
from app.video_gen import generate_audio
from dotenv import load_dotenv

load_dotenv()

def test_generation():
    print("--- Testing Video Script Generation ---")
    query = "インクが出ない"
    print(f"Query: {query}")
    
    script = get_video_script(query)
    print("\n[Generated Script]")
    print(script[:500] + "..." if len(script) > 500 else script)
    
    if not script:
        print("FAILED: Script is empty.")
        return

    print("\n--- Testing TTS ---")
    audio_b64 = generate_audio(script[:100]) # Generate for first 100 chars to save time
    if audio_b64:
        print(f"SUCCESS: Audio generated ({len(audio_b64)} chars base64)")
    else:
        print("FAILED: Audio generation failed.")

if __name__ == "__main__":
    test_generation()
