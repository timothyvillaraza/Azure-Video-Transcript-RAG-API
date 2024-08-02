import azure.functions as func
import logging
import json
# Services
from services.video_rag.api.services.chat_message_service import ChatMessageService
# Requests/Response
from services.video_rag.api.functions.models.get_chat_message_history_request import GetChatMessageHistoryRequest
from services.video_rag.api.functions.models.get_chat_message_history_response import GetChatMessageHistoryResponse


# App Registration
bp = func.Blueprint()

# Service Registration
# TODO: Create Message Service
_messageService = ChatMessageService()

@bp.function_name('GetChatMessageHistory')
@bp.route(route="getchatmessagehistory", methods=[func.HttpMethod.POST])
async def get_chat_message_history(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Log for Azure App Insights
        logging.info('Python HTTP trigger function processed a request.')
        
        # Parse request body
        request = GetChatMessageHistoryRequest(**req.get_json())

        # Validate Request
        # Validation logic

        # Service Layer Call
        # List[BaseMessage] type? Or maybe List[MessageModel] if we go down the custom message class route
        get_chat_message_history_model = await _messageService.get_chat_message_history_async(request.session_id)
        
        # Map to response
        get_message_history_response = GetChatMessageHistoryResponse(
            session_id=get_chat_message_history_model.session_id
            messages=get_message_history_model.messages,
        )
        
        return func.HttpResponse(get_message_history_response.model_dump_json(), status_code=200)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse("Error Message", status_code=400)
    