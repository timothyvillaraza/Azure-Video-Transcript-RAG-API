from pydantic import BaseModel

class GetMessageHistoryRequest(BaseModel):
    session_id: str