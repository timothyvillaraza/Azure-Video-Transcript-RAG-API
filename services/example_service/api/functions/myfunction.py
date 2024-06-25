import azure.functions as func
import logging

bp = func.Blueprint()

@bp.function_name('FirstBlueprintFunction')
@bp.route(route="blueprint")
def first_blueprint_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
            "This is a blueprint function.",
            status_code=200
    )