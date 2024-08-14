import os
from typing import List
import psycopg
from langchain_openai import ChatOpenAI
from langchain_postgres import PostgresChatMessageHistory
from langchain.docstore.document import Document
from langchain_core.messages.base import BaseMessage

class ChatMessageRepository:
    def __init__(self):
        # LLM Model
        self.chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv('OPENAI_KEY'))
        
        # Establish a synchronous connection to the database
        # (or use psycopg.AsyncConnection for async)
        self.sync_connection = psycopg.connect(os.getenv('PG_CONNECTION_STRING'))
        
        # Create the table schema (only needs to be done once)
        self.table_name = os.getenv('LANGCHAIN_CHAT_MESSAGE_TABLE_NAME')
        PostgresChatMessageHistory.create_tables(self.sync_connection, self.table_name)

    async def get_chat_message_history_async(self, session_id) -> List[BaseMessage]:     
        # Connection interface to langchain managed conversation history
        pg_chat_message_history = PostgresChatMessageHistory(self.table_name, session_id, sync_connection=self.sync_connection)
        
        return pg_chat_message_history.get_messages() # TODO: For whatever reason, ids are always returned as None. langchain_chat_message message column (type jsonb) has an id attribute that is always null which is possibly the reason why.
    