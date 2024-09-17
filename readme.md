# About the Project

This proof of concept project is designed to explore and demonstrate the integration of Retrieval Augmented Generation (RAG), Azure deployments, and CI/CD practices. The backend is fully developed and deployable, ready to be integrated with a front-end application for seamless interaction. The application provides session-based private conversations without requiring user accounts and features a chatbot that uses transcripts, pulled from user-specified YouTube URLs, to answer questions.

### Key Features

- **Retrieval Augmented Generation (RAG) Chatbot:**
  - Users can provide a list of YouTube URLs, and the server pulls the video transcripts based on those URLs.
  - The chatbot uses these transcripts as the source of context for answering user queries.
  - Generates responses based on the provided transcripts, allowing for contextually relevant and accurate answers.

- **Server-Side Session Management:**
  - Custom-built functionality that allows users to have private conversations without needing to create an account.
  - Manages the creation and tracking of user sessions.
  - Handles session authorization and expiration.
  - Includes automatic cleanup of expired sessions and related data.

- **Deployable Backend:**
  - The backend is fully deployable and ready for integration with a front-end application.
  - CI/CD pipeline setup is streamlined using Azure's Deployment Center.

# Project Architecture

### Resume Data Flow
![Untitled Diagram](https://github.com/user-attachments/assets/546ec618-c3e8-4e5a-93b7-bb050bb09159)

### Reference Architecture
- Reference Architecture from BlackSlope Architecture .NET framework
  - Read More about it here: [Introducing BlackSlope](https://medium.com/slalom-build/introducing-black-slope-a-dotnet-core-reference-architecture-from-slalom-build-3f1452eb62ef)
- Note: There is a lot of leftover or unneeded structure as the project developed.

### Dependencies
- Python 3.11.2
- LangChain (Will deprecate as LangChain v2 is poorly documented and seems unready for production use, very poor Postgres integration)
- Azure Functions Python V2 Model
- PGVector Extension on PostgreSQL
- SQLAlchemy + Alembic![Uploading Resume RAG (1).jpg…]()


### OpenAI LLM and Embeddings
- Will have to specify which ones later.

# Starting Project

1. Use Python environment
2. Python 3.11.2
3. Run `func start` on the root directory
4. Install dependencies using `pip install -r requirements.txt`
5. Create `local.settings.json`:
   ```json
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
   ```
6. Run `func start` on the root directory (if port 7073 is taken, run `func start --port 5004` or any other port).
7. To use a different port by default, update `local.settings.json`:
   ```json
   {
     "Host": {
       "LocalHttpPort": 5004
     }
   }
   ```
8. Debug with Python using F5.

### Environment Variables (As of 08/13/2024)
- Set the following environment variables:
  ```bash
  OPENAI_KEY=''

  PG_VECTOR_DRIVER='postgresql+psycopg'
  PG_VECTOR_USER=''
  PG_VECTOR_PASSWORD=''
  PG_VECTOR_HOST=''
  PG_VECTOR_PORT=''
  PG_VECTOR_DATABASE_NAME=''
  PG_VECTOR_CONNECTION_STRING='postgresql+psycopg://[rest of string]'

  PG_CONNECTION_STRING='postgresql://[rest of string]'

  SESSION_EXPIRE_MINUTES='15'
  LANGCHAIN_CHAT_MESSAGE_TABLE_NAME='langchain_chat_message'
  ```

### Create a Session
- Call the `get session` endpoint.

### Reference Videos
- [Learn Azure Functions Python V2 (Local Setup and Examples)](https://www.youtube.com/watch?v=I-kodc4bs4I)
- [Learn Azure Functions Python V2 (Part 2: Deploy, Configure, and Use in Azure)](https://www.youtube.com/watch?v=_349bwtFkE8)

# Azure Infra Setup

1. There's a DeployResources project.
2. Use the `azd something` command on `DeployResources/deploy-functions-resources.ps1`, setting unique names.
3. Set environment variables for the function app (see Starting Project section).
4. Create PostgreSQL DB then add extension from the portal side:
   - Connect and run SQL query: `{SQL QUERY FOR EXTENSION VECTOR HERE}`
5. Deploy after local development: `func azure functionapp publish myapplications`

### Troubleshooting
- If no functions are appearing on the portal:
  - Ensure the project works locally, and fix errors there.
  - See the [Debugging on Deploy](#debugging-on-deploy) section.

# Local Development

1. Use Python environment.
2. Run `func start` for local development.
3. Set up Azurite emulator for blob storage or other containers locally.
4. Run the Azurite command to start it.

# Code Structure

- Bulk of code is in `services/video_rag`. The entry point (and good starting point when browsing code) would be any of the function files.

### Azure Function Python V2 Model Functions
- Only using blueprints:
  - `services/myservice/api/functions/myfunctions.py`
  - Register blueprint in `function_app.py`:
    ```python
    from services.example_service.api.functions.myfunction import bp as blueprint_service_test_functions
    from services.video_rag.api.functions.video_rag_functions import bp as blueprint_video_rag_functions

    app = func.FunctionApp()

    # Register other functions
    app.register_blueprint(blueprint_service_test_functions)
    app.register_blueprint(blueprint_video_rag_functions)
    ```

# Sessions

### Session Verification
- At every endpoint call (except `GetOrCreateSession` endpoint), sessions are checked with the `SessionAuthorizer`.
- Globally, every session has an expiration time determined by the environment variable `SESSION_EXPIRE_MINUTES`.

### Creating Sessions
- `GetOrCreateSession`
  - Provides new session ID if:
    - **Invalid ID**: The requested one doesn't return a session from the database.
    - **Session Expired**: The session exists but the `create_date` is older than `create_date + [ENV VARIABLE] SESSION_EXPIRE_MINUTES`.

### Session Expiration
- Cron job `session_expire_timer`:
  - Runs at midnight and checks for every session that has expired and will cascade delete any sessions.
  - For local testing, change `run_on_startup=False` to `True` so that the function triggers every time the project runs locally.
  - **Note**: 
    - Any of the LangChain-managed tables (denoted by `langchain_pg_[table name]`) must be handled through the LangChain libraries.
    - Example: `langchain_pg_collection` and `langchain_pg_embedding`. These must be managed through the LangChain-PGVector class: `PGVector`.
    - A full list of non-SQLAlchemy-managed tables can be found in `alembic_migrations/config/autogenerate_excluded_tables.py`.

# CI/CD

### Setting Up Pipeline
- GitHub Actions were used to set up the CI/CD pipeline.
  - Basic authentication was used so that creating new identities wasn't needed.
- The initial project structure was created with `func init {project name} --python v2`.
  - This makes it easy to use the deployment center on the Azure portal to deploy it.
- On the portal, use the deployment center on the Azure portal and connect to the GitHub repo.

### Deploying
- `requirements.txt` is important for the dependencies.
- Run `pip freeze > requirements.txt` to generate it.

### Troubleshooting
- If endpoints aren't showing up in the function app on the portal, ensure there are no errors when running the app locally.
- If endpoints are still not showing up despite working locally, see the [Debugging on Deploy](#debugging-on-deploy) section.
  - The debugger for seeing exceptions is hidden and not easy to find.

# Testing Endpoints

- Get Function URL from Azure from the Function App.
- Testing locally, no auth is needed (something about auth level not being anonymous but function level).

# Set Environment Variables on Function App

- Set `OPENAI_KEY` and other PGVector keys.

# Database

### How to Initialize All Database Tables
1. (If the project was run previously)
   - Drop all tables from the database.
   - Delete all Alembic migrations in `alembic_migrations/versions` (the `versions` folder should be empty).

2. (To initialize SQLAlchemy/Alembic managed DB tables)
   - Run `alembic revision --autogenerate -m "init"`
   - Run `alembic upgrade head`

3. (To initialize LangChain managed DB tables)
   - Use the `SaveVideoTranscript` endpoint.

### Adding Database Tables

#### Setting Up Models on a Brand New Service
- Uses SQLAlchemy and Alembic.
- Ensure to create a shared `declarative_base()` defined in `services/[service name]/repositories/models/__init__.py`.
  - Any models should import from that.

  ```python
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

  # Import all other modules in the current package for Alembic's autogenerate in env.py target_metadata.
  # This ensures that all models are registered with the Base metadata, allowing Alembic to detect
  # and include all tables when generating migration scripts without the need to manually import each model.
  package_dir = os.path.dirname(__file__)
  for (module_loader, name, ispkg) in pkgutil.iter_modules([package_dir]):
      importlib.import_module(f"\${name}")
  ```

  ```python
  # mymodel.py
  from services.video_rag.api.repositories.models import Base
  from sqlalchemy.orm import Mapped, mapped_column
  from datetime import datetime

  class VideoDto(Base):
      __tablename__ = 'video'
      video_id: Mapped[int] = mapped_column(primary_key=True)
      user_id: Mapped[str]
      create_date: Mapped[datetime]
  ```

- Ensure in `alembic/env.py`, set `target_metadata = autogenerate_base_metadatas`.

- Edit `autogenerate_base_metadatas.py` to include models from different services:
```python
# Include Base Metadatas 
from services.video_rag.api.repositories.models import Base as video_rag_base

autogenerate_base_metadatas = [
    video_rag_base.metadata,
    # Other service models
]
```

### Steps to Ensure Alembic Autogenerates Migrations Correctly

1. Ensure the shared `Base` is defined in the `models/__init__.py` file.
   
2. Import all modules in the current package dynamically to register all models:
   - Use `pkgutil` and `importlib` to import all models in the `__init__.py` file.

3. Define your models to inherit from the shared `Base`:
   - Example model definition in `mymodel.py` as shown above.

4. Configure Alembic to use the shared metadata in `env.py`:
   - Set `target_metadata = autogenerate_base_metadatas`.

5. Ensure all service models are included in `autogenerate_base_metadatas.py`:
   - Import `Base` from each service and add its metadata to the `autogenerate_base_metadatas` list.

6. Run Alembic commands to generate and apply migrations:
   - Use `alembic revision --autogenerate -m "message"` to generate migration scripts.
   - Use `alembic upgrade head` to apply the migrations to the database.

### Adding Tables to an Existing Service

- Uses SQLAlchemy and Alembic.

Ensure the shared `declarative_base()` is defined in `services/[service name]/repositories/models/__init__.py`.

Define your models to inherit from the shared `Base`:

```python
# mymodel.py
from services.video_rag.api.repositories.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class VideoDto(Base):
    __tablename__ = 'video'
    video_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    create_date: Mapped[datetime]
```

Make sure that in the `alembic/env.py`, set `target_metadata = autogenerate_base_metadatas` from `autogenerate_base_metadatas`.

### Steps to Ensure Alembic Autogenerates Migrations Correctly

1. Ensure the shared `Base` is defined in the `models/__init__.py` file.
   
2. Import all modules in the current package dynamically to register all models:
   - Use `pkgutil` and `importlib` to import all models in the `__init__.py` file.

3. Define your models to inherit from the shared `Base`:
   - Example model definition in `mymodel.py` as shown above.

4. Configure Alembic to use the shared metadata in `env.py`:
   - Set `target_metadata = autogenerate_base_metadatas`.

5. Run Alembic commands to generate and apply migrations:
   - Use `alembic revision --autogenerate -m "message"` to generate migration scripts.
   - Use `alembic upgrade head` to apply the migrations to the database.

### To Ignore Tables Not Managed by SQLAlchemy During the Alembic Autogenerate Process

Update your `env.py` and create an `autogenerate_excluded_tables.py` file.

`env.py`:

```python
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
```

`autogenerate_excluded_tables.py`:

```python
autogenerate_excluded_tables = [
    # LangChain Managed Tables
    "langchain_pg_collection",
    "langchain_pg_embedding"
]
```

### Deploying Migrations (Putting Tables Online)

1. In `env.py`, add the connection string in `.env`.
2. Run `alembic revision --autogenerate -m "message"`.
3. Run `alembic upgrade head`.

# Debugging on Deploy

### How to View Exception Logs
- See this [GitHub issue comment](https://github.com/Azure/azure-functions-python-worker/issues/1262#issuecomment-2119241515).

- Example: Helped debug function endpoints working locally but not showing up after being deployed. There was a runtime error on app startup that wouldn't show up anywhere.
