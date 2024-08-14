import os

autogenerate_excluded_tables = [
    # LangChain Managed Tables
    "langchain_pg_collection",
    "langchain_pg_embedding",
    
    # Langchain conversation memory
    os.getenv('LANGCHAIN_CHAT_MESSAGE_TABLE_NAME')
]