import os
import psycopg
from typing import List
from services.video_rag.api.repositories.models.session_dto import SessionDto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

class SessionRepository:
    def __init__(self):
        # Establish a synchronous connection to the database
        # (or use psycopg.AsyncConnection for async)
        self.sync_connection = psycopg.connect(os.getenv('PG_CONNECTION_STRING'))
        
        # SQLALCHEMY CONNECTION
        self.engine = create_engine(os.getenv('PG_CONNECTION_STRING'))
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    async def get_session_by_id_async(self, session_id: str) -> SessionDto:     
        try:
            # TODO: Is this async?
            session_dto = select(SessionDto).where(SessionDto.session_id == session_id and SessionDto.is_active == True)
            
        except Exception as e:
            self.session.rollback() 
        
        return session_dto