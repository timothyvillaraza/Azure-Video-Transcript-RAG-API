from pydantic import BaseModel

class RagQueryRequest(BaseModel):
    query: str