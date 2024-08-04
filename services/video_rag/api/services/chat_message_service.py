from langchain_core.messages.base import BaseMessage
from typing import Dict, List
# Repositories
from services.video_rag.api.repositories.chat_message_repository import ChatMessageRepository
# Models
from services.video_rag.api.services.models.chat_message_history_model import ChatMessageHistoryModel
from services.video_rag.api.services.models.chat_message_history.chat_message_model import ChatMessageModel

from services.video_rag.api.services.enums.chat_message_type_enum import ChatMessageTypeEnum

class ChatMessageService:
    def __init__(self):
        self._chat_message_repository = ChatMessageRepository()

    async def get_chat_message_history_async(self, session_id) -> ChatMessageHistoryModel:
        # Get Relevant Documents from Repository
        chat_history_dtos = await self._chat_message_repository.get_chat_message_history_async(session_id)
        
        # Map to modelk
        chat_message_history_model = self._get_chat_message_history_model(session_id, chat_history_dtos)
        
        return chat_message_history_model
    
    # Mappers
    def _get_chat_message_history_model(self, session_id: str, chat_history_dtos: List[BaseMessage])-> ChatMessageHistoryModel:
        # Create a List[ChatMessageModel] from every BaseMessage
        chat_message_models = [self._get_chat_message_model(msg) for msg in chat_history_dtos]
        
        chat_message_history_model = ChatMessageHistoryModel(session_id, chat_message_models)
        
        return chat_message_history_model
    
    def _get_chat_message_model(self, src: BaseMessage)-> ChatMessageModel:
        chat_message_type_id = ChatMessageTypeEnum.HUMAN if src.type is "human" else  ChatMessageTypeEnum.AI
        
        chat_message_model = ChatMessageModel(src.id, chat_message_type_id, src.content)
        
        return chat_message_model
    