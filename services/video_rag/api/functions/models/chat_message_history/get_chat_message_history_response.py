from pydantic import BaseModel
from typing import List
from services.video_rag.api.functions.models.chat_message_history.chat_message_response import ChatMessageResponse

class GetChatMessageHistoryResponse(BaseModel):
    session_id: str
    chat_messages: List[ChatMessageResponse]