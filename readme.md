# Project Name

## Overview

This project is based on the BlackSlope Architecture for .NET framework and includes Azure Functions using Python V2 Model with Python 3.11.2. It leverages Lang Chain, OpenAI LLM, and PGVector Extension on PostgreSQL.

## Project Architecture

- **Reference Architecture**: [BlackSlope Architecture](https://medium.com/slalom-build/introducing-black-slope-a-dotnet-core-reference-architecture-from-slalom-build-3f1452eb62ef)
- **Core Technologies**:
  - Azure Functions Python V2 Model
  - Python 3.11.2
  - Lang Chain
  - OpenAI LLM and Embeddings
  - PGVector Extension on PostgreSQL

- **Code Structure**:
  - Bulk of code in `services/video_rag/api/functions/video_rag_functions.py`
  - Creating New Endpoints:
    - Only using blueprints
    - Example path: `services/myservice/api/functions/myfunctions.py`
    - Register blueprint in `function_app.py`:
      ```python
      from services.example_service.api.functions.myfunction import bp as blueprint_service_test_functions
      from services.video_rag.api.functions.video_rag_functions import bp as blueprint_video_rag_functions

      app = func.FunctionApp()

      # Register other functions
      app.register_blueprint(blueprint_service_test_functions)
      app.register_blueprint(blueprint_video_rag_functions)
      ```

## Getting Started

1. **Setup Python Environment**:
   - Python 3.11.2
   - Install dependencies:
     ```sh
     pip install -r requirements.txt
     ```

2. **Start the Project**:
   - Start Azure Functions:
     ```sh
     func start
     ```
   - If port 7071 is taken, use another port:
     ```sh
     func start --port 5004
     ```
   - Debug with Python F5.

3. **Reference Videos**:
   - [Learn Azure Functions Python V2 (Local Setup and Examples)](https://www.youtube.com/watch?v=I-kodc4bs4I)
   - [Learn Azure Functions Python V2 (Part 2: Deploy, Configure, and Use in Azure)](https://www.youtube.com/watch?v=_349bwtFkE8)

## Azure Infrastructure Setup

1. **Deploy Resources**:
   - Use the `azd` command on `DeployResources/deploy-functions-resources.ps1` (set unique names as needed).

2. **PostgreSQL Setup**:
   - Create PostgreSQL DB and add PGVector extension from the portal side.
   - Connect and run SQL query to add extension:
     ```sql
     -- SQL QUERY FOR EXTENSION VECTOR HERE
     ```

3. **Deploy to Azure**:
   - Publish application:
     ```sh
     func azure functionapp publish myapplications
     ```

4. **Troubleshooting**:
   - If no functions appear on the portal, ensure they work locally first and fix any errors.

## Local Development

1. **Start Local Development**:
   - Use Python environment:
     ```sh
     func start
     ```
   - Set up Azurite emulator for local blob storage or other containers:
     ```sh
     azurite
     ```

## Setting Up Pipeline

1. **Deployment Center**:
   - On the Azure portal, use the deployment center to connect to the GitHub repository.

## Deploying

1. **Freeze Requirements**:
   ```sh
   pip freeze > requirements.txt
   ```

## Testing Endpoints

1. **Get Function URL**:
   - Retrieve from Azure Function App for endpoint testing.
   - For local testing, no authentication is needed if the auth level is set to function.

## Environment Variables

1. **Set on Function App**:
   - OPEN_AI_KEY and other PGVector Keys.