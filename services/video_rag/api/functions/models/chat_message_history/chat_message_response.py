from pydantic import BaseModel
from typing import Optional

class ChatMessageResponse(BaseModel):
        chat_message_id: Optional[int]
        chat_message_type_id: int
        content: str