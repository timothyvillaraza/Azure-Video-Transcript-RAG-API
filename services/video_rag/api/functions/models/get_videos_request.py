from pydantic import BaseModel

class GetVideosRequest(BaseModel):
    session_id: str