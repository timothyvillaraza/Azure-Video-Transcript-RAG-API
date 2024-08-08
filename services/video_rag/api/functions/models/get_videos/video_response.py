from pydantic import BaseModel
from datetime import datetime

class VideoResponse(BaseModel):
    video_id: int
    external_video_id: str
    session_id: str
    create_date: datetime
    is_active: bool