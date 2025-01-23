from fastapi import APIRouter, HTTPException
from app.models.document import ClearResponse,ClearRequest
from app.controllers.general_controller import GeneralController

router = APIRouter()
controller = GeneralController()

@router.post("/clear", response_model=ClearResponse)
async def clear_vector_store(request: ClearRequest):
    """
    API endpoint to clear all keys associated with a given index in the Redis vector store.
    """
    try:
        response = controller.clear_vector_store(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

