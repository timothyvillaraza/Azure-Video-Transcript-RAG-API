import os
import psycopg
from typing import List
from services.video_rag.api.repositories.models.video_dto import VideoDto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

class VideoRepository:
    def __init__(self):
        # Establish a synchronous connection to the database
        # (or use psycopg.AsyncConnection for async)
        self.sync_connection = psycopg.connect(os.getenv('PG_CONNECTION_STRING'))
        
        # SQLALCHEMY CONNECTION
        self.engine = create_engine(os.getenv('PG_CONNECTION_STRING'))
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
    async def get_videos_by_session_id_async(self, session_id: str) -> List[VideoDto]:     
        query = select(VideoDto).where(VideoDto.session_id == session_id and VideoDto.is_active == True)
        
        try:    
            # TODO: Is this async?
            video_dtos = [video for video in self.session.execute(query).scalars().all()]
            
            return video_dtos
        except Exception as e:
            self.session.rollback() 
