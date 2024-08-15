import logging
from typing import Dict, List
# from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound


class YouTubeTranscriptService:    
    def __init__(self):
        pass
    
    def get_youtube_transcripts_async(self, video_ids: List[str]) -> Dict:
        transcripts = {}
        failed_video_ids = []

        transcripts, failed_video_ids = YouTubeTranscriptApi.get_transcripts(video_ids, continue_after_error=True)

        return transcripts, failed_video_ids