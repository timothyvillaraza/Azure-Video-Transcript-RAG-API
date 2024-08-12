# Services
from services.video_rag.api.services.session_service import SessionService

# Service Registration
_sessionService = SessionService()

class SessionAuthorizer:
    @staticmethod
    async def authorize_async(session_id: str):
        session_model = await _sessionService.get_session_by_id_async(session_id)
        
        if session_model is None:
            unauthorized_session_error = PermissionError(f"The session id '{session_id}' is expired or invalid")
            unauthorized_session_error.status_code = 401 
            
            raise unauthorized_session_error
