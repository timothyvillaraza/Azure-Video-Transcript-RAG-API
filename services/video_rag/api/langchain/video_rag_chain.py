import os
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_postgres import PostgresChatMessageHistory
import psycopg

class VideoRAGChain:
    def __init__(self, session_id):
        # Establish a synchronous connection to the database
        # (or use psycopg.AsyncConnection for async)
        self.sync_connection = psycopg.connect(os.getenv('PG_CONNECTION_STRING'))
        
        # Create the table schema (only needs to be done once)
        self.table_name = "chat_message"
        PostgresChatMessageHistory.create_tables(self.sync_connection, self.table_name)
        
        # Persistent Chat History on DB
        self.chat_history = PostgresChatMessageHistory(
            self.table_name,
            session_id,
            sync_connection=self.sync_connection
        )
        
    def get_inference_with_context(self, context):
        pass
        