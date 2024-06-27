Project Architecture:
    Reference Architecture from BlackSlope Architecture .NET framework
        Read More about it here: https://medium.com/slalom-build/introducing-black-slope-a-dotnet-core-reference-architecture-from-slalom-build-3f1452eb62ef

    A lot of left over or straignt up uneeded structure
    Azure Functions Python V2 Model
    Python 3.11.2
    bulk of code in services/video_rag/api/functions/video_rag_functions.py
    Lang Chain
    OpenAI LLM and Embeddings (will have to specify which ones later)
    PGVector Extension on PG Vector
    
    Creating New Endpoints
        - Only using blueprints
        - services/myservice/api/functions/myfunctions.py
        - Registed blueprint in function_app.py
            from services.example_service.api.functions.myfunction import bp as blueprint_service_test_functions
            from services.video_rag.api.functions.video_rag_functions import bp as blueprint_video_rag_functions

            app = func.FunctionApp()

            # Register other functions
            app.register_blueprint(blueprint_service_test_functions)
            app.register_blueprint(blueprint_video_rag_functions)


Starting Project:
    Use python environment
    Python 3.11.2
    func start on root directory
    pip install from requirements.txt
    func start (if 7071 is taken, do func start --port 5004 or any other port)
        Or add   "Host": {
                "LocalHttpPort": 5004
            }
        to localsettings.json
    Can debug with Python F5
    Set environment variables
        OPENAI_KEY

        PG_VECTOR_DRIVER = 'postgresql+psycopg'
        PG_VECTOR_USER
        PG_VECTOR_PASSWORD
        PG_VECTOR_HOST
        PG_VECTOR_PORT
        PG_VECTOR_DATABASE_NAME

    

    Reference Videos:
        Learn Azure Functions Python V2 (Local Setup and Examples)
        https://www.youtube.com/watch?v=I-kodc4bs4I

        
        Learn Azure Functions Python V2 (Part 2: Deploy, Configure, and Use in Azure)
        https://www.youtube.com/watch?v=_349bwtFkE8

Azure Infra Setup:
    There's a DeployResources project
    azd something command on DeployResouces/deploy-functions-resources.ps1, would have to set unique names
    Set environment variables for the function app

    Create Postgres DB then add extension from portal side
        - Connect and run SQL query: {SQL QUERY FOR EXTENSION VECTOR HERE}

    Deploy after local development: func azure functionapp publish myapplications

    Trouble Shooting:
        No functions appearing on portal
            - Probably not working locally as well, fix errors there

Local Development:
    use python environment
    func start for local development
    Set up azurite emulator for blob storage or other containers locally
    run azurite command to start it

Setting Up Pipeline:
    On the portal, use the deployment center and connect to the github repo

Deploying:
    pip freeze > requirements.txt

Testing Endpoints:
    Get Function URL from Azure from the Function App
    Testing locally, no auth is needed (somthing something auth level is not anonymous but function level)

Set Environment Variables on Function App:
    OPEN_AI KEY and a bunch of other PGVector Keys
