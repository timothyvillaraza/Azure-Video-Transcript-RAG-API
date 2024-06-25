import azure.functions as func
from services.video_rag.api.functions.models.query_request import QueryRequest
from services.video_rag.api.functions.models.query_response import QueryResponse
import logging
import json

bp = func.Blueprint()

@bp.function_name('query')
@bp.route(route="query", methods=[func.HttpMethod.GET])
def query(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        request = QueryRequest(**req.get_json())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

    # Service Layer
    response = QueryResponse()
    response.response = f"Your Request: {request.query}"
    
    return func.HttpResponse(
            json.dumps(response.__dict__),
            status_code=200
    )