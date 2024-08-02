from pydantic import BaseModel

class GetInferenceResponse(BaseModel):
    response: str