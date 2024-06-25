import azure.functions as func
import logging
import csv
import codecs
from services.example_service.api.functions.myfunction import bp as blueprint_service_test_functions
from services.video_rag.api.functions.video_rag_functions import bp as blueprint_video_rag_functions

app = func.FunctionApp()
app.register_blueprint(blueprint_service_test_functions)
app.register_blueprint(blueprint_video_rag_functions)

@app.function_name('FirstHTTPFunction')
@app.route(route="firstroute", auth_level=func.AuthLevel.FUNCTION)
def first_http_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
            "Success!!",
            status_code=200
    )

@app.function_name('SecondHTTPFunction')
@app.route(route="secondroute", auth_level=func.AuthLevel.FUNCTION)
def first_http_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting the second HTTP Function Request.')
    
    name = req.params.get('name')
    if name:
        message = f"Hello, {name}, so glad this function worked!"
    else:
        message = "Hello, no name was provided"
    
    return func.HttpResponse(
        message,
        status_code=200
    )
    
# @app.function_name(name="MyFirstBlobFunction")
# @app.blob_trigger(arg_name="myblob",
#                    path="newcontainer/People.csv",
#                    connection="AzureWebJobsStorage")
# def my_first_blob_function(myblob: func.InputStream):
#     logging.info(f"Python blob Function triggered after the People.csv file was uploaded to the newcontainer. So cool!!!! \n"
#                 f"Printing the name of the blob path: {myblob.name}"
#                 )
    
# @app.function_name(name="ReadFileBlobFunction")
# @app.blob_trigger(arg_name="readfile",
#                    path="newcontainer/People2.csv",
#                    connection="AzureWebJobsStorage")
# def read_file_blob_function(readfile: func.InputStream):
#     reader=csv.reader(codecs.iterdecode(readfile,'utf-8'))
#     for line in reader:
#         print(line)