from datetime import datetime

class VideoModel:
    def __init__(self, video_id: int, external_video_id: str, session_id: str, create_date: datetime, is_active: bool):
        self.video_id = video_id
        self.external_video_id = external_video_id
        self.session_id = session_id
        self.create_date = create_date
        self.is_active = is_active