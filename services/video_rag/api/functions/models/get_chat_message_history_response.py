from langchain_core.messages import BaseMessage
from pydantic.v1 import BaseModel
from typing import List

class GetChatMessageHistoryResponse(BaseModel):
    session_id: str
    chat_messages: List[BaseMessage]