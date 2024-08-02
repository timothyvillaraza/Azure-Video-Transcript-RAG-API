from langchain_core.messages.base import BaseMessage
from typing import Dict, List
# Repositories
from services.video_rag.api.repositories.chat_message_repository import ChatMessageRepository
# Models
from services.video_rag.api.services.models.chat_message_model import ChatMessageModel

class ChatMessageService:
    def __init__(self):
        self._chat_message_repository = ChatMessageRepository()
    
    async def get_chat_message_history_async(self, session_id) -> ChatMessageModel:
        # Get Relevant Documents from Repository
        chat_history = await self._chat_message_repository.get_chat_message_history_async(session_id)
        
        chat_message_model = ChatMessageModel(session_id=session_id, chat_messages=chat_history)
        
        return chat_message_model