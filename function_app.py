import azure.functions as func
import logging
import csv
import codecs
from services.example_service.api.functions.myfunction import bp as blueprint_service_test_functions
from services.video_rag.api.functions.video_rag_functions import bp as blueprint_video_rag_functions

app = func.FunctionApp()

# Register other functions
app.register_blueprint(blueprint_service_test_functions)
app.register_blueprint(blueprint_video_rag_functions)