from pydantic import BaseModel
from typing import List

class SaveVideoTranscriptRequest(BaseModel):
    session_id: str
    video_ids: List[str]