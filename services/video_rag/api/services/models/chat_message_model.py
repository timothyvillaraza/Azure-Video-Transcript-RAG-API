from typing import List
from langchain_core.messages import BaseMessage

class ChatMessageModel:
    def __init__(self, session_id: str, chat_messages: List[BaseMessage]):
        self.session_id = session_id
        self.chat_messages = chat_messages