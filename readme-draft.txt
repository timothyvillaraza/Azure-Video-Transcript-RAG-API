About the Project
    This proof of concept project is designed to explore and demonstrate the integration of Retrieval Augmented Generation (RAG), Azure deployments, and CI/CD practices. The backend is fully developed and deployable, ready to be integrated with a front-end application for seamless interaction. The application provides session-based private conversations without requiring user accounts and features a chatbot that uses transcripts, pulled from user-specified YouTube URLs, to answer questions.

Key Features
    Retrieval Augmented Generation (RAG) Chatbot
        Users can provide a list of YouTube URLs, and the server pulls the video transcripts based on those URLs. The chatbot uses these transcripts as the source of context for answering user queries. Generates responses based on the provided transcripts, allowing for contextually relevant and accurate answers.

    Server-Side Session Management
        Custom-built functionality that allows users to have private conversations without needing to create an account. Manages the creation and tracking of user sessions. Handles session authorization and expiration. Includes automatic cleanup of expired sessions and related data.

    Deployable Backend
        The backend is fully deployable and ready for integration with a front-end application. CI/CD pipeline setup is streamlined using Azure's Deployment Center.

Project Architecture:
    Reference Architecture from BlackSlope Architecture .NET framework
        Read More about it here: https://medium.com/slalom-build/introducing-black-slope-a-dotnet-core-reference-architecture-from-slalom-build-3f1452eb62ef

    A lot of left over or straignt up uneeded structure
    
    Dependencies
        Python 3.11.2
        LangChain (Will deprecate as LangChain v2 is poorly documented and seems unready for production use, very poor postgres integration)
        Azure Functions Python V2 Model
        PGVector Extension on PG Vector
        SQLAlchemy + Alembic

    OpenAI LLM and Embeddings (will have to specify which ones later)

Starting Project:
    Use python environment
    Python 3.11.2
    func start on root directory
    pip install from requirements.txt
    Create local.settings.json
    {
        "IsEncrypted": false,
        "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python"
        },
        "Host": {
            "LocalHttpPort": 7073
        }
    }
    func start on root directory
    pip install from requirements.txt

    func start (if 7073 is taken, do func start --port 5004 or any other port)
        Or add   "Host": {
                "LocalHttpPort": 5004
            }
        to localsettings.json
    Can debug with Python F5
    
    # Values as of 08/13/2024
    Set environment variables
        OPENAI_KEY = ''

        PG_VECTOR_DRIVER = 'postgresql+psycopg'
        PG_VECTOR_USER = ''
        PG_VECTOR_PASSWORD = ''
        PG_VECTOR_HOST = ''
        PG_VECTOR_PORT = ''
        PG_VECTOR_DATABASE_NAME = ''
        PG_VECTOR_CONNECTION_STRING = 'postgresql+psycopg://[rest of string]'

        PG_CONNECTION_STRING = 'postgresql://[rest of string]'

        SESSION_EXPIRE_MINUTES = '15'
        LANGCHAIN_CHAT_MESSAGE_TABLE_NAME = 'langchain_chat_message'

    Create a session by calling the get session endpoint

    Reference Videos:
        Learn Azure Functions Python V2 (Local Setup and Examples)
        https://www.youtube.com/watch?v=I-kodc4bs4I
        
        Learn Azure Functions Python V2 (Part 2: Deploy, Configure, and Use in Azure)
        https://www.youtube.com/watch?v=_349bwtFkE8

Azure Infra Setup:
    There's a DeployResources project
    azd something command on DeployResouces/deploy-functions-resources.ps1, would have to set unique names
    Set environment variables for the function app (see starting project section)

    Create Postgres DB then add extension from portal side
        - Connect and run SQL query: {SQL QUERY FOR EXTENSION VECTOR HERE}

    Deploy after local development: func azure functionapp publish myapplications

    Troubleshooting:
        No functions appearing on portal
            - Probably not working locally as well, fix errors there
            - See [DEBUGGING ON DEPLOY] section

Local Development:
    use python environment
    func start for local development
    Set up azurite emulator for blob storage or other containers locally
    run azurite command to start it

Code Structure
    Bulk of code in services/video_rag, the entry point (and good starting point when browsing code) would be any of the function files

    Azure Function Python v2 Model Functions (See Local Development for examples)
    - Only using blueprints
    - services/myservice/api/functions/myfunctions.py
    - Register blueprint in function_app.py
        from services.example_service.api.functions.myfunction import bp as blueprint_service_test_functions
        from services.video_rag.api.functions.video_rag_functions import bp as blueprint_video_rag_functions

        app = func.FunctionApp()

        # Register other functions
        app.register_blueprint(blueprint_service_test_functions)
        app.register_blueprint(blueprint_video_rag_functions)

[SESSIONS]
    Session Verification
        At every endpoint call (except GetOrCreateSession endpoint) sessions are checked with the SessionAuthorizer.
    
        Globally, every session has an expiration time determined by the environment variable SESSION_EXPIRE_MINUTES 

    Creating Sessions
        GetOrCreateSession
            Provides new session id if
                Invalid ID: The requested one doesn't return a session from the database
                Session Expired: The session exists but the create_date is older than create_date + [ENV VARIABLE] SESSION_EXPIRE_MINUTES

    Session Expiration
        chron job session_expire_timer
            Runs at midnight and checks for every session that has expired and will cascade delete any sessions.
            Locally testing, I changed run_on_startup=False to True so that the funciton triggers every time I locally run the project 
        NOTE:
            Any of the langchain manged tables (denoted by langchain_pg_[table name]) has to be handled through the langchain libraries
            An example of a langchain managed db tables are langchain_pg_collection and langchian_pg_emebdding. These have to be managed through langchain-pgvector class: PGVector
            A full list of non sqlalchemy managed tables can be found in alembic_migrations/config/autogenerate_excluded_tables.py

CI/CD
    Setting Up Pipeline:
        GitHub actions was used to setup the CI/CD pipeline
            I forgot which option it is, but I think the option is basic authentication so that creating new identies wasn't needed
        The initial project structure was made with func init {project name} --python v2
            - This makes it pretty easy to use the deployment center on azure portal to deploy it 
        On the portal, use the deployment center on the azure portal and connect to the github repo

    Deploying:
        requirements.txt is important for the dependencies
        pip freeze > requirements.txt

    Troubleshooting
        If endpoints aren't showing up in the functionapp on the portal, make sure there are no errors when running the app locally
        If endpoints are still not showing up despite it working locally, see the [DEBUGGING ON DEPLOY] section
            - The debugger for seeing exceptions is kind of hidden and not easy to find

Testing Endpoints:
    Get Function URL from Azure from the Function App
    Testing locally, no auth is needed (somthing something auth level is not anonymous but function level)

Set Environment Variables on Function App:
    OPEN_AI KEY and a bunch of other PGVector Keys

[DATABASE]
    [How to initailize all database tables]
        1. (If project was ran previously)
            Drop all tables from db
            Delete all alembic migrations in alembic_migrations/versions (versions folder should be empty)

        2. (To initialize sqlalchemy/alembic managed db tables)
            alembic revision --autogenerate -m "init"
            alembic migrate head

        3. (To initalize langchain managed db tables)
            Use the SaveVideoTranscript End Point

    [Adding Database Tables]
        [Setting up models on a brand new service]
            Uses SQLAlchemy and Alembic

            Make sure to create a shared declarative_base() defined in services/[service name]/repositories/models/__init__.py
            Any models should import from that

            example:

                # models __init__.py 
                import pkgutil
                import importlib
                import os
                from sqlalchemy.orm import declarative_base

                # Import this in alembic_migrations/config/autogenerate_base_metadatas.py
                from services.video_rag.api.repositories.models import Base as video_rag_base

                autogenerate_base_metadatas = [
                    video_rag_base.metadata,
                    # Other service models
                ]

                # Import all other modules in current package for Alembic's autogenerate in env.py target_metadata.
                # This ensures that all models are registered with the Base metadata, allowing Alembic to detect
                # and include all tables when generating migration scripts without the need to manually import each model.
                package_dir = os.path.dirname(__file__)
                for (module_loader, name, ispkg) in pkgutil.iter_modules([package_dir]):
                    importlib.import_module(f"{__name__}.{name}")

                # mymodel.py
                from services.video_rag.api.repositories.models import Base
                from sqlalchemy.orm import Mapped, mapped_column
                from datetime import datetime

                class VideoDto(Base):
                    __tablename__ = 'video'
                    video_id: Mapped[int] = mapped_column(primary_key=True)
                    user_id: Mapped[str]
                    create_date: Mapped[datetime]

            Make sure that in the alembic env.py, we set target_metadata = autogenerate_base_metadatas from autogenerate_base_metadatas

            Edit autogenerate_base_metadatas.py to include models from different services
                Example:
                # Include Base Metadatas 
                from services.video_rag.api.repositories.models import Base as video_rag_base

                autogenerate_base_metadatas = [
                    video_rag_base.metadata,
                    # Other service models
                ]

            Steps to ensure Alembic autogenerates migrations correctly:

                1. Ensure the shared Base is defined in the models/__init__.py file.
                
                2. Import all modules in the current package dynamically to register all models:
                    - Use pkgutil and importlib to import all models in the __init__.py file.

                3. Define your models to inherit from the shared Base:
                    - Example model definition in mymodel.py as shown above.

                4. Configure Alembic to use the shared metadata in env.py:
                    - Set target_metadata = autogenerate_base_metadatas.

                5. Ensure all service models are included in autogenerate_base_metadatas.py:
                    - Import Base from each service and add its metadata to the autogenerate_base_metadatas list.

                6. Run Alembic commands to generate and apply migrations:
                    - Use alembic revision --autogenerate -m "message" to generate migration scripts.
                    - Use alembic upgrade head to apply the migrations to the database.

        [Adding Tables to existing service]
            Uses SQLAlchemy and Alembic

            Ensure the shared declarative_base() is defined in services/[service name]/repositories/models/__init__.py

            Define your models to inherit from the shared Base:

                # mymodel.py
                from services.video_rag.api.repositories.models import Base
                from sqlalchemy.orm import Mapped, mapped_column
                from datetime import datetime

                class VideoDto(Base):
                    __tablename__ = 'video'
                    video_id: Mapped[int] = mapped_column(primary_key=True)
                    user_id: Mapped[str]
                    create_date: Mapped[datetime]

            Make sure that in the alembic env.py, we set target_metadata = autogenerate_base_metadatas from autogenerate_base_metadatas

            Steps to ensure Alembic autogenerates migrations correctly:

                1. Ensure the shared Base is defined in the models/__init__.py file.
                
                2. Import all modules in the current package dynamically to register all models:
                    - Use pkgutil and importlib to import all models in the __init__.py file.

                3. Define your models to inherit from the shared Base:
                    - Example model definition in mymodel.py as shown above.

                4. Configure Alembic to use the shared metadata in env.py:
                    - Set target_metadata = autogenerate_base_metadatas.

                5. Run Alembic commands to generate and apply migrations:
                    - Use alembic revision --autogenerate -m "message" to generate migration scripts.
                    - Use alembic upgrade head to apply the migrations to the database.

        [To ignore tables that are not managed by SQLAlchemy during the Alembic autogenerate process]
        Update your `env.py` and create an `autogenerate_excluded_tables.py` file.
            env.py:

                from alembic_migrations.config.autogenerate_excluded_tables import autogenerate_excluded_tables

                target_metadata = autogenerate_base_metadatas

                for metadata in target_metadata:
                    print("Metadata tables:", metadata.tables.keys())

                # Function to exclude database tables not managed by SQLAlchemy
                def include_object(object, name, type_, reflected, compare_to):
                    print(f"Processing object: name={name}, type={type_}, reflected={reflected}")
                    if type_ == "table":
                        if name in autogenerate_excluded_tables:
                            print(f"Excluding table: {name}")
                            return False
                        else:
                            print(f"Including table: {name}")
                            return True
                    return True

            autogenerate_excluded_tables.py:

                autogenerate_excluded_tables = [
                    # LangChain Managed Tables
                    "langchain_pg_collection",
                    "langchain_pg_embedding"
                ]

    Deploying Migrations (Putting Tables Online)
        env.py put in connection string in .env
        alembic revision --autogenerate -m "message"
        alembic upgrade head

[DEBUGGING ON DEPLOY]
    How to view exception logs:
        https://github.com/Azure/azure-functions-python-worker/issues/1262#issuecomment-2119241515

        Example: Helped me debug function endpoints working locally but not showing up after being deployed. There was a run time error on app start up that wouldn't show up anywhere.
