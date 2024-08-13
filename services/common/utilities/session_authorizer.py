import os
from datetime import datetime, timedelta
# Services
from services.video_rag.api.services.session_service import SessionService

# Service Registration
_sessionService = SessionService()

class SessionAuthorizer:
    @staticmethod
    async def authorize_async(session_id: str):
        session_model = await _sessionService.get_session_by_id_async(session_id)
        
        if session_model is None or is_expired(session_model.create_date):
            unauthorized_session_error = PermissionError(f"The session id '{session_id}' is expired or invalid")
            unauthorized_session_error.status_code = 401 
            
            raise unauthorized_session_error

# Helper Functions
def is_expired(time: datetime):
    time_difference = datetime.now() - time
    
    return time_difference >= timedelta(minutes=int(os.getenv('SESSION_EXPIRE_MINUTES')))
