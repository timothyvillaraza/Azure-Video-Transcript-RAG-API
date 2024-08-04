from typing import List
from services.video_rag.api.services.models.chat_message_history.chat_message_model import ChatMessageModel

class ChatMessageHistoryModel:
    def __init__(self, session_id: str, chat_messages: List[ChatMessageModel]):
        self.session_id = session_id
        self.chat_messages = chat_messages