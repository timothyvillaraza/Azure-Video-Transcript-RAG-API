from pydantic import BaseModel
from datetime import datetime

class GetSessionResponse(BaseModel):
    session_id: str
    create_date: datetime