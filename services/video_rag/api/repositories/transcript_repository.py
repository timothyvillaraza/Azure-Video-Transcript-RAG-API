import os
import logging
from typing import List
from langchain.docstore.document import Document
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from services.video_rag.api.repositories.models.transcript_embeddings_dto import TranscriptEmbeddingsDto

# Ensure the environment variables are correctly set
PG_VECTOR_DRIVER = os.getenv('PG_VECTOR_DRIVER')
PG_VECTOR_USER = os.getenv('PG_VECTOR_USER')
PG_VECTOR_PASSWORD = os.getenv('PG_VECTOR_PASSWORD')
PG_VECTOR_HOST = os.getenv('PG_VECTOR_HOST')
PG_VECTOR_PORT = os.getenv('PG_VECTOR_PORT')
PG_VECTOR_DATABASE_NAME = os.getenv('PG_VECTOR_DATABASE_NAME')

class TranscriptRepository:
    def __init__(self):
        self.open_ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_KEY"))
        self.collection_name = 'transcripts'
        
        # Construct the connection string
        self.CONNECTION_STRING = f"{PG_VECTOR_DRIVER}://{PG_VECTOR_USER}:{PG_VECTOR_PASSWORD}@{PG_VECTOR_HOST}:{PG_VECTOR_PORT}/{PG_VECTOR_DATABASE_NAME}"
        
        self.vectorstore = PGVector(
            embeddings=self.open_ai_embeddings,
            collection_name=self.collection_name,
            connection=self.CONNECTION_STRING,
            use_jsonb=True,
        )
        
    def save_transcript_embeddings(self, documents: List[Document]) -> TranscriptEmbeddingsDto:
        successful_video_ids = []
        failed_video_ids = []

        for video_id, docs_list in documents.items():
            try:
                self.vectorstore.add_documents(docs_list)
                successful_video_ids.append(video_id)
            except Exception as e:
                failed_video_ids.append(video_id)
                print(f"Error adding documents for video_id: {video_id}. Error: {e}")

        # Transcript DTO
        return TranscriptEmbeddingsDto(successful_video_ids, failed_video_ids)
    
    def drop_all_embeddings(self) -> bool:
        try:
            self.vectorstore.drop_tables()
            logging.info("Successfully dropped all embeddings.")
            return True
        except Exception as e:
            logging.error(f"Failed to drop embeddings: {str(e)}")
            return False