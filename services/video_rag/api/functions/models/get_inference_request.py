from pydantic import BaseModel

class GetInferenceRequest(BaseModel):
    user_id: str
    query: str