import os
import langchain
from typing import List
from langchain_openai import OpenAIEmbeddings

from services.video_rag.api.services.models.save_video_transcript_model import SaveVideoTranscriptmodel
from services.video_rag.api.services.youtube_transcript_service import YouTubeTranscriptService

class VideoRagService:
    def __init__(self):
        self._youtubeTranscriptService = YouTubeTranscriptService()
    
    def save_video_transcript(self, video_ids: List[str]):
        tempModelResponse = SaveVideoTranscriptmodel()

        # Get Transcripts
        temp = self._youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        # Chunk Transcripts
        # Embed Transcripts
        # Save Transcripts to PG Vector
        
        return tempModelResponse
    
    def get_video_transcript(self, video_ids: List[str]):
        tempModelResponse = SaveVideoTranscriptmodel()

        self._youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        # Chunk Transcripts
        # Embed Transcripts
        # Save Transcripts to PG Vector
        
        return tempModelResponse