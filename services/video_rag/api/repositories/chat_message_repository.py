import os
from typing import List
import psycopg
from jinja2 import Template
from langchain.prompts import SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_postgres import PostgresChatMessageHistory
from langchain.docstore.document import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.messages.base import BaseMessage

class ChatMessageRepository:
    def __init__(self):
        # LLM Model
        self.chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv('OPENAI_KEY'))
        
        # Establish a synchronous connection to the database
        # (or use psycopg.AsyncConnection for async)
        self.sync_connection = psycopg.connect(os.getenv('PG_CONNECTION_STRING'))
        
        # Create the table schema (only needs to be done once)
        self.table_name = "chat_message"
        PostgresChatMessageHistory.create_tables(self.sync_connection, self.table_name)

    async def get_chat_message_history_async(self, session_id) -> List[BaseMessage]:     
        # Connection interface to langchain managed conversation history
        pg_chat_message_history = PostgresChatMessageHistory(self.table_name, session_id, sync_connection=self.sync_connection)
        
        return pg_chat_message_history.messages