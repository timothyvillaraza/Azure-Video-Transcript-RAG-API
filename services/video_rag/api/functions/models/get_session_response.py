from pydantic import BaseModel
from datetime import datetime

class GetOrCreateSessionResponse(BaseModel):
    session_id: str
    create_date: datetime