from pydantic import BaseModel

class GetChatMessageHistoryRequest(BaseModel):
    session_id: str