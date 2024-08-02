from pydantic import BaseModel
from datetime import datetime

class GetInferenceRequest(BaseModel):
    session_id: str
    query: str
    create_date: datetime