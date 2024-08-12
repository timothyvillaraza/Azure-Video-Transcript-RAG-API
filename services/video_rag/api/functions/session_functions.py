import azure.functions as func
import logging
# Services
from services.video_rag.api.services.session_service import SessionService

# Requests/Response
from services.video_rag.api.functions.models.get_session_request import GetOrCreateSessionRequest
from services.video_rag.api.functions.models.get_session_response import GetOrCreateSessionResponse

# App Registration
bp = func.Blueprint()

# Service Registration
_sessionService = SessionService()
 
@bp.function_name('GetOrCreateSession')
@bp.route(route="getorcreatesession", methods=[func.HttpMethod.POST])
async def get_or_create_session(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Log for Azure App Insights
        logging.info('Python HTTP trigger function processed a request.')
        
        # Parse request body
        request = GetOrCreateSessionRequest(**req.get_json())
        
        # Service Layer Call
        session_model = await _sessionService.get_or_create_session_by_id_async(request.session_id)
        
        # Map to response
        response = GetOrCreateSessionResponse(
            session_id=session_model.session_id,
            create_date=session_model.create_date
        )
        
        # Set status code: 200 if session was found, 201 if a new session was created
        status_code = 200 if request.session_id == session_model.session_id else 201
        
        return func.HttpResponse(response.model_dump_json(), status_code=status_code)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse(str(e), status_code=getattr(e, 'status_code', 400))
    