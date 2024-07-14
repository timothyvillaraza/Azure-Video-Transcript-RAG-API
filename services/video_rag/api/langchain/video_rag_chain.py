
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

class VideoRAGChain:
    def __init__(self):
        # LLM Model
        self.chat_model = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv('OPENAI_KEY'))
        
        # Establish a synchronous connection to the database
        # (or use psycopg.AsyncConnection for async)
        self.sync_connection = psycopg.connect(os.getenv('PG_CONNECTION_STRING'))
        
        # Create the table schema (only needs to be done once)
        self.table_name = "chat_message"
        PostgresChatMessageHistory.create_tables(self.sync_connection, self.table_name)
        
    def get_session_history_memory(self, session_id) -> ConversationBufferMemory:
        pg_chat_message_history = PostgresChatMessageHistory(self.table_name, session_id, sync_connection=self.sync_connection)
        
        return ConversationBufferMemory(llm=self.chat_model, chat_memory=pg_chat_message_history, memory_key='history', max_token_limit=100, return_messages=True)

        
    def get_inference_with_context(self, session_id: str, user_query: str, context: List[Document]):
        # Define the system template using Jinja2
        system_template = """
        SYSTEM PROMPT:
        Only answer responding with the information from the TRANSCRIPT CHUNK. TIME STAMPS MUST BE INCLUDED.
        
        Your response also must include all sources of your answer.
            - Video transcript sources need time stamps from the TRANSCRIPT CHUNK provided below
            
        If no time stamp can be provided in the final answer, respond with "There is not enough information provided."

        TRANSCRIPT CHUNK:
        {{ context }}
        """
        
        # Format the context for the prompt
        context_content = " ".join([doc.page_content for doc in context])
        
        # Render the system message with context
        formatted_system_message = Template(system_template).render(context=context_content)
        
        # Create a SystemMessagePromptTemplate from the formatted system message
        system_message_prompt = SystemMessagePromptTemplate.from_template(formatted_system_message)
        
        # Define the complete prompt template
        prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,  # System message with context
            MessagesPlaceholder(variable_name="history"),  # Placeholder for chat history
            HumanMessagePromptTemplate.from_template("{input}")  # Human message prompt
        ])
        
        # Initialize the conversation chain with the formatted prompt
        runnable = ConversationChain(
            prompt=prompt,
            llm=self.chat_model,
            memory=self.get_session_history_memory(session_id),
            verbose=True
        )

        # Use the chain with memory
        llm_response = runnable.invoke({
            "input": user_query
        })
        
        return llm_response['response']
        