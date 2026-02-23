
import os
import fitz  # PyMuPDF
import base64
from io import BytesIO
from PIL import Image

def extract_page_as_base64(pdf_path: str, page_num: int, dpi: int = 150) -> str:
    """
    Extracts a specific page from a PDF and returns it as a base64 encoded PNG.
    page_num is 1-indexed.
    """
    try:
        if not os.path.exists(pdf_path):
            return ""
            
        doc = fitz.open(pdf_path)
        # fitz is 0-indexed
        if page_num < 1 or page_num > len(doc):
            return ""
            
        page = doc.load_page(page_num - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        
        # Convert pixmap to image and then to base64
        img_data = pix.tobytes("png")
        base64_str = base64.b64encode(img_data).decode('utf-8')
        doc.close()
        return base64_str
    except Exception as e:
        print(f"Error extracting PDF page: {e}")
        return ""

def get_manual_path(manual_name: str) -> str:
    """Helper to get absolute path of a manual."""
    from .rag import MANUALS_DIR
    return os.path.join(MANUALS_DIR, manual_name)
