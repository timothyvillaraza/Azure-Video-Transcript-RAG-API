from pydantic import BaseModel
from typing import Optional

class GetOrCreateSessionRequest(BaseModel):
    session_id: Optional[str]