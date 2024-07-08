from pydantic import BaseModel
from datetime import datetime

class GetInferenceRequest(BaseModel):
    user_id: str
    query: str
    create_date: datetime