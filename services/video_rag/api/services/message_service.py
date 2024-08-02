from langchain_core.messages.base import BaseMessage
from typing import Dict, List
# Repositories
from services.video_rag.api.repositories.message_repository import MessageRepository
# Models
from services.video_rag.api.services.models.inference_model import InferenceModel


class MessageService:
    def __init__(self):
        self._message_repository = MessageRepository()
    
    async def get_message_history_async(self, session_id) -> List[BaseMessage]:
        # Get Relevant Documents from Repository
        message_dtos = await self._messageRepository.get_message_history_async(session_id)
        
        inference_model = InferenceModel(response=llm_response)
        
        return inference_model