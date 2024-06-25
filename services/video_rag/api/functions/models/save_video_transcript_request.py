from pydantic import BaseModel
from typing import List

class SaveVideoTranscriptRequest(BaseModel):
    video_ids: List[str]