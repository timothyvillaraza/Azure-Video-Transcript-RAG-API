import azure.functions as func
import logging
import json
# Services
from services.video_rag.api.services.video_rag_service import VideoRagService
# Requests/Response
from services.video_rag.api.functions.models.get_inference_request import GetInferenceRequest
from services.video_rag.api.functions.models.get_inference_response import GetInferenceResponse
from services.video_rag.api.functions.models.save_video_transcript_request import SaveVideoTranscriptRequest
from services.video_rag.api.functions.models.save_video_transcript_response import SaveVideoTranscriptResponse


# App Registration
bp = func.Blueprint()

# Service Registration
videoRagService = VideoRagService()

@bp.function_name('SaveVideoTranscript')
@bp.route(route="savevideotranscript", methods=[func.HttpMethod.POST])
def save_video_transcript(req: func.HttpRequest) -> func.HttpResponse:
    # Log for Azure App Insights
    logging.info('Python HTTP trigger function processed a request.')

    # Parse request body
    try:
        request = SaveVideoTranscriptRequest(**req.get_json())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse(
            "Error Message",
            status_code=400
        )
        
    # Validate Request

    # Service Layer Call
    saveVideoTranscriptModel = videoRagService.save_video_transcript(request)
    
    # Map to response
    # response = response_model
    response = SaveVideoTranscriptResponse()
    response.response = f"Your Request: {saveVideoTranscriptModel.query}"
    
    return func.HttpResponse(
            json.dumps(response.__dict__),
            status_code=200
    )

@bp.function_name('GetInference')
@bp.route(route="getinference", methods=[func.HttpMethod.GET])
def get_inference(req: func.HttpRequest) -> func.HttpResponse:
    # Log for Azure App Insights
    logging.info('Python HTTP trigger function processed a request.')

    # Parse request body
    try:
        request = GetInferenceRequest(**req.get_json())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse(
            "Error Message",
            status_code=400
        )
        
    # Validate Request

    # Service Layer Call
    # response_model = service.method()
    
    # Map to response
    # response = response_model
    response = GetInferenceResponse()
    response.response = f"Your Request: {request.query}"
    
    return func.HttpResponse(
            json.dumps(response.__dict__),
            status_code=200
    )