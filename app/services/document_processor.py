from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings 
from langchain_redis import RedisVectorStore
from app.config import settings
from app.utils.text_processor import TextProcessor
from typing import List, Dict, Any
import os

class DocumentProcessor:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in environment variables")

        self.text_processor = TextProcessor()
        self.embeddings = None
        self.vector_store = None

    def create_prerequisites(self,index_name):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = RedisVectorStore(
            redis_url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            index_name=index_name,
            embeddings=self.embeddings
        )
        
        self.text_splitter = SemanticChunker(
            embeddings=self.embeddings
        )
    
    def process_pdf(self, file_path: str, source_name: str, index_name: str) -> Dict[str, Any]:
        """
        Process a PDF document through the complete pipeline:
        1. Load and extract text using PyPDFLoader
        2. Clean the text
        3. Split into semantic chunks
        4. Create embeddings and store in Redis
        """
        self.create_prerequisites(index_name=index_name)

        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        for doc in documents:
            # print(doc.metadata)
            doc.page_content = self.text_processor.clean_text(doc.page_content)
            doc.metadata["source"] = source_name

        chunks = self.text_splitter.split_documents(documents)

        try:
            ids = self.vector_store.add_documents(chunks)
            return {
                "message": f"Successfully processed {source_name}",
                "total_pages": len(documents),
                "total_chunks": len(chunks),
                # "document_ids": ids
            }
        except Exception as e:
            print("Some Error")
            raise Exception(f"Error storing documents in Redis: {str(e)}")
    
    def similarity_search(self, query: str, k: int = 5,index_name="") -> List[Dict[str, Any]]:
        """
        Search for similar documents in the vector store
        """
        try:
            self.create_prerequisites(index_name=index_name)
            cleaned_query = self.text_processor.clean_text(query)

            docs_with_scores = self.vector_store.similarity_search_with_score(
                cleaned_query,
                k=k
            )
            results = []
            for doc, score in docs_with_scores[::-1]:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)  # Convert numpy float to Python float
                })
            
            return results
        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")

document_processor = DocumentProcessor() 