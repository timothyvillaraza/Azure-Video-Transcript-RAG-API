from pydantic import BaseModel
from typing import List
from services.video_rag.api.functions.models.get_videos.video_response import VideoResponse

class GetVideosResponse(BaseModel):
    videos: List[VideoResponse]