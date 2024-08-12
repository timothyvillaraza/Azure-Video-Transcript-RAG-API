import azure.functions as func
import logging
# Services
from services.video_rag.api.services.chat_message_service import ChatMessageService

# Utilities
from services.common.utilities.session_authorizer import SessionAuthorizer

# Requests/Response
from services.video_rag.api.functions.models.chat_message_history.get_chat_message_history_request import GetChatMessageHistoryRequest
from services.video_rag.api.functions.models.chat_message_history.get_chat_message_history_response import GetChatMessageHistoryResponse
from services.video_rag.api.functions.models.chat_message_history.chat_message_response import ChatMessageResponse 


# App Registration
bp = func.Blueprint()

# Service Registration
_messageService = ChatMessageService()

@bp.function_name('GetChatMessageHistory')
@bp.route(route="getchatmessagehistory", methods=[func.HttpMethod.GET])
async def get_chat_message_history(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Log for Azure App Insights
        logging.info('Python HTTP trigger function processed a request.')
        
        # Parse request body
        request = GetChatMessageHistoryRequest(**req.get_json())
        
        # Authorize Session
        await SessionAuthorizer.authorize_async(request.session_id)

        # Validate Request

        # Service Layer Call
        chat_message_history_model = await _messageService.get_chat_message_history_async(request.session_id)
        
        # Map to response
        get_message_history_response = GetChatMessageHistoryResponse(
            session_id=chat_message_history_model.session_id,
            chat_messages=[ChatMessageResponse(chat_message_id=src.chat_message_id, chat_message_type_id=src.chat_message_type_id, content=src.content) for src in chat_message_history_model.chat_messages]
        )
        
        return func.HttpResponse(get_message_history_response.model_dump_json(), status_code=200)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse(str(e), status_code=getattr(e, 'status_code', 400))
    
