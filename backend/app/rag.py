import os
import json
import time
from typing import List, Optional
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from google.generativeai.caching import CachedContent

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANUALS_DIR = os.path.join(BASE_DIR, "..", "manuals")

# Global variables
_full_context_cache = None
_gemini_cache: Optional[any] = None
_cache_expiry = 0

def get_full_context():
    """Reads all PDF manuals and returns full text with page numbers."""
    global _full_context_cache
    if _full_context_cache is not None:
        return _full_context_cache
        
    try:
        if not os.path.exists(MANUALS_DIR):
            print(f"DEBUG: Manuals directory not found at {MANUALS_DIR}")
            return ""

        print("Loading PDF manuals locally...")
        manual_files = [f for f in os.listdir(MANUALS_DIR) if f.lower().endswith('.pdf')]
        
        # Deduplicate by basename (ignore case/extension) or size to skip redundant versions
        seen_sizes = set()
        unique_manuals = []
        for f in manual_files:
            f_path = os.path.join(MANUALS_DIR, f)
            f_size = os.path.getsize(f_path)
            if f_size not in seen_sizes:
                seen_sizes.add(f_size)
                unique_manuals.append(f_path)
            else:
                print(f"DEBUG: Skipping redundant manual '{f}' (size mismatch or identical to already loaded)")

        all_pages = []
        for f_path in unique_manuals:
            try:
                print(f"DEBUG: Parsing {os.path.basename(f_path)}...")
                loader = PyPDFLoader(f_path)
                all_pages.extend(loader.load())
            except Exception as e:
                print(f"DEBUG: Failed to parse {f_path}: {e}")

        if not all_pages:
            print("DEBUG: No documents were found/loaded from manuals directory")
            return ""
            
        # Format: "Page 1: Content..."
        formatted_pages = []
        for doc in all_pages:
            page_num = doc.metadata.get('page', 0) + 1 
            source = os.path.basename(doc.metadata.get('source', 'Manual'))
            content = doc.page_content.replace('\n', ' ')
            formatted_pages.append(f"[[Source: {source} | Page: {page_num}]]\n{content}\n")
            
        _full_context_cache = "\n".join(formatted_pages)
        print(f"Loaded full context: {len(_full_context_cache)} chars from {len(all_pages)} pages")
        return _full_context_cache
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error loading full context: {e}")
        return ""

def _ensure_cache():
    """Ensures that the Gemini Context Cache is created and valid."""
    global _gemini_cache, _cache_expiry
    
    # Configure GenAI globally/idempotently
    if os.environ.get("GOOGLE_API_KEY"):
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    else:
        print("GOOGLE_API_KEY not found in environment.")
        return None

    full_context = get_full_context()
    if not full_context:
        print("Full context is empty, cannot create cache.")
        return None

    # Check if cache exists and is valid
    current_time = time.time()
    if _gemini_cache and current_time < _cache_expiry:
        return _gemini_cache

    print("Context Caching is disabled or not supported in this environment.")
    return None
    # try:
    #     # Create cache
    #     _gemini_cache = genai.caching.CachedContent.create(
    #         model='models/gemini-2.0-flash-001',
    #         display_name='manual_cache',
    #         system_instruction='You are a helpful technical support assistant for Canon TS6330.',
    #         contents=[full_context],
    #         ttl=datetime.timedelta(minutes=60)
    #     )
    #     _cache_expiry = current_time + (55 * 60) # Refresh before 60 mins
    #     print(f"Cache created: {_gemini_cache.name}")
    #     return _gemini_cache
    # except Exception as e:
    #     print(f"Error creating cache: {e}")
    #     return None

import datetime

def ingest_manuals():
    """Refreshes the full context cache and Gemini cache."""
    global _full_context_cache, _gemini_cache
    _full_context_cache = None
    _gemini_cache = None # Force recreation
    
    ctx = get_full_context()
    if ctx:
        # Pre-warm cache
        _ensure_cache()
        return f"Loaded {len(ctx)} characters from manuals and updated cache."
    else:
        return "No manuals found or error loading."

def get_loaded_status():
    """Returns details about loaded manuals and context status."""
    manuals = []
    if os.path.exists(MANUALS_DIR):
        manuals = [f for f in os.listdir(MANUALS_DIR) if f.lower().endswith('.pdf')]
    
    return {
        "manuals": manuals,
        "is_context_loaded": _full_context_cache is not None,
        "context_length": len(_full_context_cache) if _full_context_cache else 0,
        "is_gemini_cached": _gemini_cache is not None
    }

def get_rag_diagnosis(query: str):
    """
    Diagnosis using Gemini Context Caching.
    """
    try:
        cache = _ensure_cache()
        
        if not cache:
            # Fallback to non-cached if cache creation failed
            print("Fallback to non-cached RAG")
            full_context = get_full_context()
            if not full_context:
                 return {
                    "probable_causes": ["Manual not loaded"],
                    "steps": ["Please upload the manual PDF."],
                    "confidence": 0.0,
                    "cautions": [],
                    "next_actions": {},
                    "disclaimer": "System not initialized.",
                    "referenced_pages": [],
                    "source_file": None
                }
            
            # Just use direct genai without cache for fallback
            # Ensure configured even if _ensure_cache returned None (though it does configure now)
            if os.environ.get("GOOGLE_API_KEY"):
                genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

            # Fallback model: use standard gemini-2.0-flash
            model = genai.GenerativeModel('gemini-2.0-flash')
            print(f"[{time.time()}] Gemini Flash Fallback Prompting...", flush=True)

            prompt = f"""
            あなたは Canon TS6330 の専門技術者です。
            以下のマニュアルを使用して、ユーザーの問題: "{query}" を診断してください。
            
            マニュアル:
            {full_context[:60000]} (Truncated if needed, but Flash handles large context well)
            
            JSON形式で回答してください:
            {{
                "probable_causes": ["原因1"],
                "confidence": 0.8,
                "steps": ["手順1"],
                "cautions": [],
                "next_actions": {{}},
                "disclaimer": "...",
                "referenced_pages": [10, 20],
                "source_file": "manual.pdf"
            }}
            IMPORTANT: "referenced_pages" MUST be a list of integers. Do NOT use strings like "P.10". Only numbers. e.g. [10, 35].
            """
            
            try:
                resp = model.generate_content(prompt)
                print(f"[{time.time()}] Gemini Flash Fallback Response Received.", flush=True)
                text = resp.text
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]
                
                data = json.loads(text)
                
                # --- NORMALIZE DATA FOR PYDANTIC ---
                # 1. Normalize steps (Ensure List[str])
                if "steps" in data:
                    new_steps = []
                    for s in data["steps"]:
                        if isinstance(s, str):
                            new_steps.append(s)
                        elif isinstance(s, dict) and "description" in s:
                             new_steps.append(s["description"])
                        elif isinstance(s, dict) and "step" in s:
                             new_steps.append(s["step"])
                        else:
                            new_steps.append(str(s))
                    data["steps"] = new_steps

                # 2. Normalize referenced_pages (Ensure List[int])
                if "referenced_pages" in data:
                    new_pages = []
                    for p in data["referenced_pages"]:
                        try:
                            if isinstance(p, int):
                                new_pages.append(p)
                            elif isinstance(p, str):
                                # Extract digits
                                import re
                                digits = re.findall(r'\d+', p)
                                if digits:
                                    new_pages.append(int(digits[0]))
                        except:
                            pass
                    data["referenced_pages"] = new_pages
                
                return data
            except Exception as e:
                print(f"[{time.time()}] Fallback Generation Error: {e}")
                import traceback
                traceback.print_exc()
                return {"probable_causes": ["Diagnosis failed (API Error)"], "steps": ["Please try again."], "confidence": 0.0, "referenced_pages": [], "next_actions": {}, "cautions": [], "disclaimer": f"Gemini Error: {str(e)}"}

        # Cached Path
        model = genai.GenerativeModel.from_cached_content(cached_content=cache)
        
        prompt = f"""
        ユーザーの課題: {query}
        
        専門用語をなるべく使わず、初心者にもわかりやすい言葉で以下のJSON形式で診断してください:
        {{
            "probable_causes": ["原因1", "原因2"],
            "confidence": 0.8,
            "steps": ["手順1", "手順2"],
            "cautions": ["注意点"],
            "next_actions": {{ "primary": "action", "secondary": [] }},
            "disclaimer": "...",
            "referenced_pages": [10, 12],
            "source_file": "TS6330.pdf"
        }}
        Important: "referenced_pages" MUST be integers extracted from [[Source: ... | Page: X]] markers.
        """
        
        try:
            response = model.generate_content(prompt)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text)
        except Exception as e:
            print(f"Cached Generation Error: {e}")
            import traceback
            traceback.print_exc()
            return {"probable_causes": ["Error (Cached)"], "steps": ["Try again."], "confidence": 0, "referenced_pages": [], "next_actions": {}, "cautions": [], "disclaimer": str(e)}

    except Exception as e:
        print(f"Outer Diagnosis Error: {e}")
        return {"probable_causes": ["System Error"], "steps": [], "confidence": 0, "referenced_pages": [], "next_actions": {}, "cautions": [], "disclaimer": str(e)}

def get_video_script(query: str):
    """
    Generates script using Gemini Context Caching or Fallback.
    """
    try:
        cache = _ensure_cache()
        if cache:
             model = genai.GenerativeModel.from_cached_content(cached_content=cache)
        else:
             print("Video Gen: Falling back to non-cached")
             if os.environ.get("GOOGLE_API_KEY"):
                genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
             model = genai.GenerativeModel('gemini-2.0-flash')
        
        # If fallback, we need context in prompt? 
        # Yes, if no cache, manual isn't loaded in model.
        # But for video script, maybe we don't need FULL manual if we have diagnosis?
        # Ideally we pass full context or the relevant parts.
        # For simplicity, let's pass context if fallback.
        
        if not cache:
            full_context = get_full_context()
            prompt = f"""
            ユーザーの質問: {query}
            マニュアル情報: {full_context[:30000]}
            
            これに対する親しみやすいラジオMC風の解説スクリプトを作成してください。
            - 挨拶と共感から始める。
            - 具体的なページ番号に言及する。
            - 1分程度。
            """
        else:
             prompt = f"""
            ユーザーの質問: {query}
            
            これに対する親しみやすいラジオMC風の解説スクリプトを作成してください。
            - 挨拶と共感から始める。
            - 具体的なページ番号に言及する。
            - 1分程度。
            """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Script Error: {e}")
        return "エラーが発生しました。"
