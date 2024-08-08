from pydantic import BaseModel

class ChatMessageResponse(BaseModel):
        chat_message_id: int
        chat_message_type_id: int
        content: str