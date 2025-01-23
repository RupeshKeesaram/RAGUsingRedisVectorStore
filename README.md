# RAG System with Langchain and Redis

This repository contains a **Retrieval-Augmented Generation (RAG)** system built using the **Langchain Framework**. The system leverages **Redis** as a vector store to store and retrieve document embeddings for efficient document retrieval tasks.

## Features

- **Langchain Framework**: Used for managing and processing the language model-based queries and responses.
- **Redis as Vector Store**: Redis is used to store document vectors and metadata, allowing for fast retrieval and efficient processing.
- **Document Processing and Uploading**: Supports uploading, processing, and indexing of documents (e.g., PDFs) in the vector store.
- **Search Functionality**: Allows querying the document store and retrieving relevant documents based on similarity scores.
- **Dockerized Application**: Easily run the entire application using Docker and Docker Compose.

## Requirements

Before running the application, ensure you have the following installed:

- **Docker**
- **Docker Compose**
- A **valid** OpenAI API key (if you are using OpenAI models)

## Setting Up the Application

1. **Clone the repository**:

   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
   
2. **Set up environment variables**:

   Create a .env file in the root directory and set the OPENAI_API_KEY variable:
   ```bash
   OPENAI_API_KEY=<your-openai-api-key>

3. **Up the application using Docker Compose**:

   With Docker Compose, you can easily spin up all the necessary services (backend, Redis, etc.). Simply run the following command:

   ```bash
   docker-compose up --build
   ```
   This will: 
   1. Pull and set up the Redis Stack image (with vector search capabilities).
   2. Build and run the backend application.
   3. Expose the backend API on port 8000 (configurable if necessary).
   

4. **Access the application**:

   Once the services are up and running, you can access the backend API at http://localhost:8000.

You can use the endpoint collections available in the repository's endpoint_collections section for interaction.
The API will allow you to upload document, search for relevant documents, and interact with the vector store.

## API Endpoints
   You can use the available endpoints for different tasks, such as:

1. **Upload Document** : Upload a PDF document and store its vectors in Redis.
2. **Search**: Search the Redis vector store for relevant documents based on a query.


Refer to the endpoint_collections section for further details on available endpoints.( There's one more API to clear the content of redis store, but that's related to this assignment, so I'm not sharing that in the collection file)
## Troubleshooting
Ensure that the Redis Stack container is running properly.
If you encounter issues with the OpenAI API, check that you have correctly set your OPENAI_API_KEY.
If the Docker Compose command fails, try running **docker-compose down** to stop all services and then re-run **docker-compose up --build**.