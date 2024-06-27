from typing import List

class TranscriptEmbeddingsDto:    
    def __init__(self, successful_video_ids: List[str], failed_video_ids: List[str]):
        self.successful_video_ids = successful_video_ids
        self.failed_video_ids = failed_video_ids
        