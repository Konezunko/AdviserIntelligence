import shutil
import os
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import json

# Load .env only if it exists (useful for local development)
if os.path.exists(os.path.join(os.path.dirname(__file__), "..", ".env")):
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
else:
    print("DEBUG: .env file not found, skipping load_dotenv. Using system env vars.", flush=True)

from .schemas import DiagnoseResponse

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Advisor Intelligence API", version="0.1.0")

# Mount manuals for static access (e.g., /manuals/TS6330.pdf)
# Better to define path here safely.
print("DEBUG: Adviser Intelligence Backend Starting...", flush=True)
MANUALS_DIR_PATH = os.path.join(os.path.dirname(__file__), "..", "manuals")
if not os.path.exists(MANUALS_DIR_PATH):
    os.makedirs(MANUALS_DIR_PATH)
    
app.mount("/manuals", StaticFiles(directory=MANUALS_DIR_PATH), name="manuals")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Advisor Intelligence Backend is running"}

# In-memory cache for video results (PoC)
_video_cache = {}

def process_video_background(query: str):
    """
    Background task to generate video assets.
    """
    print(f"DEBUG: Starting background video generation for query='{query}'", flush=True)
    try:
        from .rag import get_video_script
        from .video_gen import generate_audio, create_slides
        
        script = get_video_script(query)
        if script:
            audio_b64 = generate_audio(script)
            slides = create_slides(script)
            
            _video_cache[query] = {
                "script": script,
                "audio_base64": audio_b64,
                "slides": slides
            }
            print(f"DEBUG: Background video generation completed for query='{query}'", flush=True)
        else:
             print(f"DEBUG: Background script generation failed for query='{query}'", flush=True)
    except Exception as e:
         print(f"DEBUG: Background video generation error: {e}", flush=True)

@app.post("/api/diagnose", response_model=DiagnoseResponse)
def diagnose(
    background_tasks: BackgroundTasks,
    query: str = Form(...),
    device: Optional[str] = Form("TS6330"),
    image: Optional[UploadFile] = File(None)
):
    """
    Diagnosis endpoint.
    Accepts form-data to handle potential image uploads alongside JSON data.
    """
    try:
        # Use RAG Logic
        from .rag import get_rag_diagnosis
        import uuid
        
        # If image is present, we might want to do something, but for now RAG depends on text
        print(f"DEBUG: Calling get_rag_diagnosis with query='{query}'", flush=True)
        result = get_rag_diagnosis(query)
        print(f"DEBUG: get_rag_diagnosis returned type: {type(result)}", flush=True)
        
        # Add background task for video
        background_tasks.add_task(process_video_background, query)
        
        # Enrich result
        result["video_status"] = "processing"
        result["request_id"] = str(uuid.uuid4())
        
        return DiagnoseResponse(**result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Diagnose Endpoint Error: {e}", flush=True)
        # Return a fallback response or raise error detailed
        # FOr debugging, raise detailed error
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

@app.post("/api/ingest")
def ingest_manual():
    from .rag import ingest_manuals
    msg = ingest_manuals()
    msg = ingest_manuals()
    return {"status": "completed", "message": msg}

@app.get("/api/status")
def get_system_status():
    from .rag import get_loaded_status
    return get_loaded_status()

@app.post("/api/feedback")
def feedback(result: str = Form(...), comment: Optional[str] = Form(None)):
    return {"status": "received", "thank_you": True}

@app.post("/api/upload")
async def upload_manual(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    from .rag import ingest_manuals, MANUALS_DIR
    
    try:
        if not os.path.exists(MANUALS_DIR):
            os.makedirs(MANUALS_DIR)

        # Sanitize filename (just mostly basename)
        filename = os.path.basename(file.filename)
        file_path = os.path.join(MANUALS_DIR, filename)
        
        print(f"DEBUG: Uploading file to {file_path}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        background_tasks.add_task(ingest_manuals)
        
        return {"status": "uploaded", "filename": filename, "message": "Ingestion started in background"}

    except Exception as e:
        print(f"Upload Error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/generate_video")
async def generate_video(query: str = Form(...)):
    """
    Generates an 'Audio Overview' video (slides + audio).
    """
    from .rag import get_video_script
    from .video_gen import generate_audio, create_slides
    
    # Check cache first
    if query in _video_cache:
        print(f"DEBUG: Returning cached video for query='{query}'", flush=True)
        return _video_cache[query]

    # 1. Generate Script (Dialogue)
    script = get_video_script(query)
    if not script:
        raise HTTPException(status_code=500, detail="Failed to generate script.")

    # 2. Generate Audio (TTS)
    audio_b64 = generate_audio(script)

    # 3. Create Slides (Placeholder or Real)
    slides = create_slides(script)
    
    # Cache it
    _video_cache[query] = {
        "script": script,
        "audio_base64": audio_b64,
        "slides": slides
    }

    return {
        "script": script,
        "audio_base64": audio_b64,
        "slides": slides
    }

@app.post("/api/generate_script")
async def generate_script(query: str = Form(...)):
    """
    Generates text-only diagnosis (Conversational Script).
    Failsafe mode when video generation errors.
    """
    from .rag import get_video_script
    
    script = get_video_script(query)
    if not script:
        raise HTTPException(status_code=500, detail="Failed to generate script.")
        
    return {"script": script}

