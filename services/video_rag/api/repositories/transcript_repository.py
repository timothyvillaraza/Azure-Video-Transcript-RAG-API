import os
import logging
from typing import List
from services.video_rag.api.repositories.models.video_dto import VideoDto
from langchain.docstore.document import Document
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from services.video_rag.api.repositories.models.transcript_embeddings_dto import TranscriptEmbeddingsDto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        
        # LANGCHAIN CONNECTION
        self.vectorstore = PGVector(
            embeddings=self.open_ai_embeddings,
            collection_name=self.collection_name,
            connection=self.CONNECTION_STRING,
            use_jsonb=True,
        )
        
        # SQLALCHEMY CONNECTION
        self.engine = create_engine(self.CONNECTION_STRING)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    # TODO: Make Async
    def save_transcript_embeddings(self, documents: List[Document]) -> TranscriptEmbeddingsDto:
        successful_video_ids = [] # IDs of videos that sucessfully generated and save embeddings
        failed_video_ids = [] # IDs of videos that failed generated and save embeddings

        for external_video_id, docs_list in documents.items():
            try:
                # Add document to db through langchain's vectorstore
                self.vectorstore.add_documents(docs_list)
                
                # Add video id to db through sqlalchemy's session
                new_video = VideoDto(external_video_id=external_video_id, user_id='TODO')
                self.session.add(new_video)
                self.session.commit()
                
                successful_video_ids.append(external_video_id)
            except Exception as e:
                failed_video_ids.append(external_video_id)
                self.session.rollback() 
                print(f"Error adding documents for video_id: {external_video_id}. Error: {e}")

        # Transcript DTO
        return TranscriptEmbeddingsDto(successful_video_ids, failed_video_ids)
    
    # TODO: Make Async
    def get_by_semantic_relevance(self, query: str, results_count: int = 1) -> List[Document]:
        # async: asimilary_search
        # TODO: Add try catch block
        return self.vectorstore.similarity_search(query, results_count)
    
    # Currently a DEBUG Function.
    def drop_all_embeddings(self) -> bool:
        try:
            self.vectorstore.drop_tables()
            logging.info("Successfully dropped all embeddings.")
            return True
        except Exception as e:
            logging.error(f"Failed to drop embeddings: {str(e)}")
            return False