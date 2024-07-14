from pydantic import BaseModel
from typing import List


class GetInferenceResponse(BaseModel):
    response: str