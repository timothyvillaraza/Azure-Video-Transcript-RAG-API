from pydantic import BaseModel
from typing import Optional

class ChatMessageResponse(BaseModel):
        chat_message_id: Optional[int] # TODO: For whatever reason, ids are always returned as None. langchain_chat_message message column (type jsonb) has an id attribute that is always null which is possibly the reason why.
        chat_message_type_id: int
        content: str