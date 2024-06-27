from pydantic import BaseModel
from typing import List

class SaveVideoTranscriptResponse(BaseModel):
    successful_video_ids: List[str]
    failed_video_ids: List[str]
