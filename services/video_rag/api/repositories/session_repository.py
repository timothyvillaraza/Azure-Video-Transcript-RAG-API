import os
import logging
import psycopg
import uuid
from datetime import datetime, timedelta
from services.video_rag.api.repositories.models.session_dto import SessionDto
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

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
            session_dto = self.session.execute(query).scalar_one_or_none()

            return session_dto
        except Exception as e:
            self.session.rollback()
            
    async def create_session_async(self) -> SessionDto:     
        try:
            # TODO: Is this async?
            session_dto = SessionDto(session_id=str(uuid.uuid4()), create_date=datetime.now(), is_active= True)
            self.session.add(session_dto)
            self.session.commit()

            return session_dto
        except Exception as e:
            self.session.rollback() 
            
    async def expire_sessions_async(self, session_lifetime_min: int) -> int:
        sessions_deleted_count = 0
        
        try:
            # Query for sessions past their lifetime
            expired_sessions_query = select(SessionDto).where(datetime.now() >= SessionDto.create_date + timedelta(minutes=session_lifetime_min))
            expired_sessions_result = self.session.execute(expired_sessions_query).scalars().all()
            expired_session_ids = [row.session_id for row in expired_sessions_result]
            
            # TODO: Long term, I would like to drop langchain and have everything managed by sqlalchemy. That way, cascade delete would properly delete all associated rows as opposed to having dlete each table by session_id.
            # Delete session ids
            if expired_session_ids:
                # Cascade Delete Sessions
                delete_sessions_query = delete(SessionDto).where(SessionDto.session_id.in_(expired_session_ids))
                delete_result = self.session.execute(delete_sessions_query)
                
                # Cascade Delete langchain collections
                for session_id in expired_session_ids:
                    self._get_vector_store(session_id).delete_collection()
                
                # Delete Chat Messages
                delete_chat_message_query = text(f"DELETE FROM {os.getenv('LANGCHAIN_CHAT_MESSAGE_TABLE_NAME')} WHERE session_id IN :ids")
                
                self.session.execute(delete_chat_message_query, {'ids': tuple(expired_session_ids)})            

                self.session.commit()
                
                sessions_deleted_count = delete_result.rowcount
        except Exception as e:
            logging.exception(f"Error expiring sessions: {e}")
            self.session.rollback()
            
        return sessions_deleted_count

    def _get_vector_store(self, session_id: str):
        open_ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_KEY"))
        
        # LANGCHAIN CONNECTION
        return PGVector(
            embeddings=open_ai_embeddings,
            collection_name=session_id,
            connection=os.getenv('PG_VECTOR_CONNECTION_STRING'),
            use_jsonb=True,
        )
