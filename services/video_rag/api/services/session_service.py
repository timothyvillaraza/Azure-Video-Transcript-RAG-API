from langchain_core.messages.base import BaseMessage
from typing import Dict, List
# Repositories
from services.video_rag.api.repositories.session_repository import SessionRepository
# Models
from services.video_rag.api.services.models.session_model import SessionModel

class SessionService:
    def __init__(self):
        self._chat_message_repository = SessionRepository()

    async def get_session_async(self, session_id) -> SessionModel:
        # Get Relevant Documents from Repository
        session_dto = await self._chat_message_repository.get_session_by_id_async(session_id)
        
        return SessionModel(session_dto.session_id, session_dto.create_date, session_dto.is_active)