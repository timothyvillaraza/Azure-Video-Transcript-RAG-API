# Repositories
from services.video_rag.api.repositories.session_repository import SessionRepository
# Models
from services.video_rag.api.services.models.session_model import SessionModel

class SessionService:
    def __init__(self):
        self._session_repository = SessionRepository()
        
    async def get_session_by_id_async(self, session_id) -> SessionModel:
        session_dto = await self._session_repository.get_session_by_id_async(session_id)
        
        if session_dto is None:
            return None
        
        return SessionModel(session_dto.session_id, session_dto.create_date, session_dto.is_active)

    async def get_or_create_session_by_id_async(self, session_id) -> SessionModel:
        session_dto = await self._session_repository.get_session_by_id_async(session_id)
        
        if session_dto is None:
            session_dto = await self._session_repository.create_session_async()
        
        return SessionModel(session_dto.session_id, session_dto.create_date, session_dto.is_active)
    
    async def expire_sessions_async(self, session_lifetime_min: int) -> int:
        sessions_deleted_count = await self._session_repository.expire_sessions_async(session_lifetime_min)
        
        return sessions_deleted_count
