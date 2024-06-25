from typing import List
from langchain.chains import Chain

from services.video_rag.api.services.models.save_video_transcript_model import SaveVideoTranscriptmodel
from services.video_rag.api.services.youtube_transcript_service import YouTubeTranscriptService

youtubeTranscriptService = YouTubeTranscriptService()

class VideoRagService:
    def __init__(self):
        # Initialize Key Value Stores
        pass
    
    def save_video_transcript(self, video_ids: List[str]):
        tempModelResponse = SaveVideoTranscriptmodel()

        youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        # Chunk Transcripts
        # Embed Transcripts
        # Save Transcripts to PG Vector
        chain = Chain(
            
        )        
        
        return tempModelResponse