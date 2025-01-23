from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.document import SearchQuery, SearchResponse, DocumentUploadResponse
from app.controllers.general_controller import GeneralController

router = APIRouter()

# Initialize the controller
controller = GeneralController()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(index_name: str, file: UploadFile = File(...)):
    """Upload a PDF document, process it, and store in vector database."""
    return await controller.upload_document(index_name=index_name, file=file)

@router.post("/search", response_model=SearchResponse)
async def search_documents(query: SearchQuery):
    """Search for relevant documents based on the query."""
    results = controller.search_documents(query=query)
    return SearchResponse(results=results)
