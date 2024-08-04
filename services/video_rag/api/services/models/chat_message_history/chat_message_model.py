from datetime import datetime
from services.video_rag.api.services.enums.chat_message_type_enum import ChatMessageTypeEnum

class ChatMessageModel:
    def __init__(self, chat_message_id: int, chat_message_type_id: ChatMessageTypeEnum, content: str):
        self.chat_message_id = chat_message_id
        self.chat_message_type_id = chat_message_type_id
        self.content = content