from datetime import datetime

class SessionModel:
    def __init__(self, session_id: str, create_date: datetime, is_active: bool):
        self.session_id = session_id
        self.create_date = create_date
        self.is_active = is_active