import os
import logging
from typing import List
from services.video_rag.api.repositories.models.video_dto import VideoDto
from services.video_rag.api.repositories.models.transcript_embeddings_dto import TranscriptEmbeddingsDto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from langchain import LangChain 

lc = LangChain(db_config={
    'host': 'your_db_host',
    'port': 'your_db_port',
    'username': 'your_db_username',
    'password': 'your_db_password',
    'database': 'your_db_name'
})



# Ensure the environment variables are correctly set
PG_VECTOR_DRIVER = os.getenv('PG_VECTOR_DRIVER')
PG_VECTOR_USER = os.getenv('PG_VECTOR_USER')
PG_VECTOR_PASSWORD = os.getenv('PG_VECTOR_PASSWORD')
PG_VECTOR_HOST = os.getenv('PG_VECTOR_HOST')
PG_VECTOR_PORT = os.getenv('PG_VECTOR_PORT')
PG_VECTOR_DATABASE_NAME = os.getenv('PG_VECTOR_DATABASE_NAME')

class MessageRepository:
    def __init__(self):
        # Construct the connection string
        self.CONNECTION_STRING = f"{PG_VECTOR_DRIVER}://{PG_VECTOR_USER}:{PG_VECTOR_PASSWORD}@{PG_VECTOR_HOST}:{PG_VECTOR_PORT}/{PG_VECTOR_DATABASE_NAME}"
        
        # SQLALCHEMY CONNECTION
        self.engine = create_engine(self.CONNECTION_STRING)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    # TODO: Make Async
    async def get_message_history_async(self, session_id) -> TranscriptEmbeddingsDto:
        successful_video_ids = [] # IDs of videos that sucessfully generated and save embeddings
        failed_video_ids = [] # IDs of videos that failed generated and save embeddings
        
        # Transcript DTO
        return TranscriptEmbeddingsDto(successful_video_ids, failed_video_ids)