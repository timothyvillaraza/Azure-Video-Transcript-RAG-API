from pydantic import BaseModel

class SaveVideoTranscriptRequest(BaseModel):
    url: str