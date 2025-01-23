from app.services.document_processor import document_processor
from app.models.document import SearchQuery, SearchResponse, DocumentUploadResponse, ClearResponse, ClearRequest
from fastapi import HTTPException, UploadFile
import tempfile
import os
from typing import List, Dict, Any
from app.clients.redis_client import redis_client


class GeneralController:
    """
    Controller class for managing document upload, search, and clearing vector store operations.

    This class provides methods to:
    1. Upload and process PDF documents, storing them in a vector database.
    2. Search for relevant documents based on a provided query.
    3. Clear vector store keys from Redis associated with a specific index.

    Methods:
        - upload_document: Upload a PDF document, process it, and store it in the vector database.
        - search_documents: Search for documents based on a query and return relevant results.
        - clear_vector_store: Clear all keys in Redis associated with a given index.
    """

    def __init__(self):
        """
        Initializes the GeneralController with the document processor and Redis client.

        This constructor sets up instances for processing documents and interacting with Redis for clearing the vector store.
        """
        self.document_processor = document_processor
        self.client = redis_client.get_redis_client()

    async def upload_document(self, index_name: str, file: UploadFile) -> DocumentUploadResponse:
        """
        Upload a PDF document, process it, and store it in the vector database.

        Args:
            index_name (str): The name of the index where the document will be stored.
            file (UploadFile): The uploaded PDF file to be processed.

        Returns:
            DocumentUploadResponse: A response indicating whether the document upload and processing were successful.

        Raises:
            HTTPException: If the file is not a PDF or if there is an error during the upload or processing of the document.
        """
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_path = temp_file.name

            try:
                result = self.document_processor.process_pdf(
                    file_path=temp_path,
                    source_name=file.filename,
                    index_name=index_name
                )
                return DocumentUploadResponse(**result)

            finally:
                os.unlink(temp_path)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def search_documents(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """
        Search for relevant documents based on the given query.

        Args:
            query (SearchQuery): A search query containing the term to search and other parameters like top_k results.

        Returns:
            List[Dict[str, Any]]: A list of documents and their associated metadata that match the query.

        Raises:
            HTTPException: If there is an error during the search or retrieval of documents.
        """
        try:
            results = self.document_processor.similarity_search(
                query=query.query,
                k=query.top_k,
                index_name=query.index_name
            )
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def clear_vector_store(self, request: ClearRequest) -> ClearResponse:
        """
        Clears all keys associated with a given index in the Redis vector store.

        Args:
            request (ClearRequest): The request object containing the index name whose keys need to be cleared.

        Returns:
            ClearResponse: A response indicating the success or failure of the clearing operation.

        Raises:
            HTTPException: If there is an error while attempting to clear the vector store keys from Redis.
        """
        index_name = request.index_name
        try:
            index_keys = self.client.keys(f"{index_name}:*")

            if index_keys:
                self.client.delete(*index_keys)
                return ClearResponse(
                    status="success",
                    message=f"Index '{index_name}' and all associated keys deleted successfully."
                )
            else:
                return ClearResponse(
                    status="not_found",
                    message=f"No keys found for index '{index_name}'."
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while clearing Redis: {str(e)}")
