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

        try:
            transcripts, failed_video_ids = YouTubeTranscriptApi.get_transcripts(video_ids, continue_after_error=True)
        except (TranscriptsDisabled, VideoUnavailable, NoTranscriptFound) as e:
            logging.error(f"An error occurred with specific video IDs: {str(e)}")
            failed_video_ids.extend(e.video_id)
        except Exception as e:
            logging.error(f"An unexpected error with the YoutubeTranscriptApi: {str(e)}")
            # If the entire call fails, consider all video_ids as failed
            failed_video_ids.extend(video_ids)

        return transcripts, failed_video_ids