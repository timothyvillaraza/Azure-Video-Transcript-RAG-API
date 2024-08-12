import azure.functions as func
import logging

# Utilities
from services.common.utilities.session_authorizer import SessionAuthorizer

# Services
from services.video_rag.api.services.video_service import VideoService
# Requests/Response
from services.video_rag.api.functions.models.get_videos.video_response import VideoResponse
from services.video_rag.api.functions.models.get_videos.get_videos_response import GetVideosResponse
from services.video_rag.api.functions.models.get_videos.get_videos_request import GetVideosRequest
from services.video_rag.api.services.models.video_model import VideoModel


# App Registration
bp = func.Blueprint()

# Service Registration
_videoService = VideoService()

@bp.function_name('GetVideos')
@bp.route(route="getvideos", methods=[func.HttpMethod.GET])
async def get_videos(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Log for Azure App Insights
        logging.info('Python HTTP trigger function processed a request.')
        
        # Parse request body
        request = GetVideosRequest(**req.get_json())
        
        # Authorize Session
        await SessionAuthorizer.authorize_async(request.session_id)

        # Validate Request
        
        # Service Layer Call
        # List[VideoModel]
        video_models = await _videoService.get_videos_by_session_id_async(request.session_id)
        
        # Map to response
        response = GetVideosResponse(
            videos=[_map_video_model(video_model) for video_model in video_models]
        )
        
        return func.HttpResponse(response.model_dump_json(), status_code=200)
    except Exception as e:        
        return func.HttpResponse(str(e), status_code=getattr(e, 'status_code', 400))

# Map VideoModel -> Video Response
def _map_video_model(video_model: VideoModel) -> VideoResponse:
    return VideoResponse(video_id=video_model.video_id,
        external_video_id=video_model.external_video_id,
        session_id=video_model.session_id,
        create_date=video_model.create_date,
        is_active=video_model.is_active
    )
