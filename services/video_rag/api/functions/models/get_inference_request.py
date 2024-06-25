from pydantic import BaseModel

class GetInferenceRequest(BaseModel):
    query: str