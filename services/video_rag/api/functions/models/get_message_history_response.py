from langchain_core.messages.base import BaseMessage
from pydantic import BaseModel
from typing import List

class GetMessageHistoryResponse(BaseModel):
    session_id: str
    messages: List[BaseMessage]