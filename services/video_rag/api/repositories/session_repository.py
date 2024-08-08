import os
import psycopg
import uuid
from datetime import datetime
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
        query = select(SessionDto).where(SessionDto.session_id == session_id and SessionDto.is_active == True)
        
        try:    
            # TODO: Is this async?
            session_dto = self.session.execute(query).scalar_one()
            
            # TODO: Could be a race condition with the above line
            # Check for existence of session
            if session_dto is None:
                session_dto = SessionDto(session_id=str(uuid.uuid4()), create_date=datetime.now(), is_active= True)
                self.session.add(session_dto)
                self.session.commit()

            return session_dto
        except Exception as e:
            self.session.rollback() 
