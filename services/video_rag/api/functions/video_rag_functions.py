import azure.functions as func
from services.video_rag.api.functions.models.rag_query_request import RagQueryRequest
from services.video_rag.api.functions.models.rag_query_response import RagQueryResponse
import logging
import json

# App Registration
bp = func.Blueprint()

# Service Registration


@bp.function_name('RagQuery')
@bp.route(route="ragquery", methods=[func.HttpMethod.GET])
def rag_query(req: func.HttpRequest) -> func.HttpResponse:
    # Log for Azure App Insights
    logging.info('Python HTTP trigger function processed a request.')

    # Parse request body
    try:
        request = RagQueryRequest(**req.get_json())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        
        return func.HttpResponse(
            "Error Message",
            status_code=400
        )
        
    # Validate Request

    # Service Layer Call
    # response_model = service.method()
    
    # Map to response
    # response = response_model
    response = RagQueryResponse()
    response.response = f"Your Request: {request.query}"
    
    return func.HttpResponse(
            json.dumps(response.__dict__),
            status_code=200
    )