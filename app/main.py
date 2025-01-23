import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("app/devenv.env")


from fastapi import FastAPI
from app.routers import document_router,redis_router


app = FastAPI(
    title="Document Vector Search API",
    description="API for processing PDF documents and performing semantic search",
    version="1.0.0"
)

# Include routers
app.include_router(document_router.router, prefix="/api/v1", tags=["documents"])
app.include_router(redis_router.router, prefix="/api/v1", tags=["redis store"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Document Vector Search API",
        "endpoints": {
            "upload": "/api/v1/upload",
            "search": "/api/v1/search"
        }
    }
