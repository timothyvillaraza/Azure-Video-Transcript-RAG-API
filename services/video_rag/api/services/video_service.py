from typing import List
# Repositories
from services.video_rag.api.repositories.video_repository import VideoRepository
# Models
from services.video_rag.api.repositories.models.video_dto import VideoDto
from services.video_rag.api.services.models.video_model import VideoModel

class VideoService:
    def __init__(self):
        self._video_repository = VideoRepository()

    async def get_videos_by_session_id_async(self, session_id) -> List[VideoModel]:
        video_dtos = await self._video_repository.get_videos_by_session_id_async(session_id)
        
        # Map List[VideoDto] -> List[VideoModel]
        video_models = [self._map_video_model(video_dto) for video_dto in video_dtos]
            
        return video_models

    # Mapper
    def _map_video_model(self, video_dto: VideoDto) -> VideoModel:
        return VideoModel(video_dto.video_id, video_dto.external_video_id, video_dto.session_id, video_dto.create_date, video_dto.is_active)
        