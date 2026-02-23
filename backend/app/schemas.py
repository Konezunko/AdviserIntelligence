from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class DiagnoseRequest(BaseModel):
    query: str = Field(..., example="コピーすると変な線が入る")
    device: Optional[str] = "TS6330"
    # image field is handled via UploadFile in the actual endpoint, so we might treat this model for JSON part or form data validation
    
class DiagnoseResponse(BaseModel):
    probable_causes: List[str]
    confidence: float
    steps: List[str]
    cautions: List[str]
    next_actions: dict
    disclaimer: str
    referenced_pages: List[int] = []
    source_file: Optional[str] = None
    visual_page_base64: Optional[str] = None
    video_status: Optional[str] = None
    request_id: Optional[str] = None
