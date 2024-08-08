import azure.functions as func
import logging
import json
# Services
from services.video_rag.api.services.session_service import SessionService
# Requests/Response
from services.video_rag.api.functions.models.get_session_request import GetSessionRequest
from services.video_rag.api.functions.models.get_session_response import GetSessionResponse


# App Registration
bp = func.Blueprint()

# Service Registration
_sessionService = SessionService()

@bp.function_name('GetSession')
@bp.route(route="getsession", methods=[func.HttpMethod.POST])
async def get_session(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Log for Azure App Insights
        logging.info('Python HTTP trigger function processed a request.')
        
        # Parse request body
        request = GetSessionRequest(**req.get_json())

        # Validate Request
        # Validation logic

        # Service Layer Call
        session_model = await _sessionService.get_session_async(request.session_id)
        
        # Map to response
        response = GetSessionResponse(
            session_id=session_model.session_id,
            create_date=session_model.create_date
        )
        
        return func.HttpResponse(response.model_dump_json(), status_code=200)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse("Error Message", status_code=400)
    
