import azure.functions as func
import logging
import json
# Services
from services.video_rag.api.services.video_rag_service import VideoRagService
# Utilities
from services.common.utilities.session_authorizer import SessionAuthorizer
# Requests/Response
from services.video_rag.api.functions.models.get_inference_request import GetInferenceRequest
from services.video_rag.api.functions.models.get_inference_response import GetInferenceResponse
from services.video_rag.api.functions.models.save_video_transcript_request import SaveVideoTranscriptRequest
from services.video_rag.api.functions.models.save_video_transcript_response import SaveVideoTranscriptResponse


# App Registration
bp = func.Blueprint()

# Service Registration
_videoRagService = VideoRagService()

@bp.function_name('SaveVideoTranscript')
@bp.route(route="savevideotranscript", methods=[func.HttpMethod.POST])
async def save_video_transcript(req: func.HttpRequest) -> func.HttpResponse:
    # Log for Azure App Insights
    logging.info('Python HTTP trigger function processed a request.')

    # Parse request body
    try:
        request = SaveVideoTranscriptRequest(**req.get_json())
        
        # Authorize Session
        await SessionAuthorizer.authorize_async(request.session_id)

        # Validate Request

        # Service Layer Call
        # TODO: Make Async
        video_transcript_model = _videoRagService.save_video_transcript_embeddings(request.session_id, request.video_ids)
        
        # Map to response
        save_video_transcript_response = SaveVideoTranscriptResponse(
            successful_video_ids=video_transcript_model.successful_video_ids,
            failed_video_ids=video_transcript_model.failed_video_ids
        )
        
        return func.HttpResponse(save_video_transcript_response.model_dump_json(), status_code=200)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse(str(e), status_code=getattr(e, 'status_code', 400))

@bp.function_name('GetInference')
@bp.route(route="getinference", methods=[func.HttpMethod.POST])
def get_inference(req: func.HttpRequest) -> func.HttpResponse:
    # Log for Azure App Insights
    logging.info('Python HTTP trigger function processed a request.')

    # Parse request body
    try:
        request = GetInferenceRequest(**req.get_json())
        # Validate Request

        # Service Layer Call
        get_inference_model = _videoRagService.get_inference(request.session_id, request.query, request.create_date)
        
        # Map to response
        # response = response_model
        get_inference_response = GetInferenceResponse(
            response=get_inference_model.response
        )
        
        return func.HttpResponse(
            get_inference_response.model_dump_json(),
            status_code=200
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    
        return func.HttpResponse(str(e), status_code=getattr(e, 'status_code', 400))