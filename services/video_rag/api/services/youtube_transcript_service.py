import logging
from typing import Dict, List
# from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscriptService:    
    def __init__(self):
        pass
    
    def get_youtube_transcripts_async(self, video_ids: List[str]) -> Dict:
        try:
            transcripts, failed_transcripts_ids = YouTubeTranscriptApi.get_transcripts(video_ids)
        except Exception as e:
            logging.error(f"An unexpected error with the YoutubeTranscriptApi: {str(e)}")

        return transcripts