from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DocumentUploadResponse(BaseModel):
    message: str
    total_pages: int
    total_chunks: int
    # ids : List[str]

class SearchResult(BaseModel):
    content: str
    score: float

class SearchQuery(BaseModel):
    query: str
    top_k: Optional[int] = 5
    index_name: str

class SearchResponse(BaseModel):
    results: List[SearchResult]

class ClearRequest(BaseModel):
    index_name : str

class ClearResponse(BaseModel):
    status : str
    message:str