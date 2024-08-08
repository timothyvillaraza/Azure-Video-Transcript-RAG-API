from pydantic import BaseModel
from typing import Optional

class GetSessionRequest(BaseModel):
    session_id: Optional[str]