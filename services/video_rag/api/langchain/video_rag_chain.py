"""
TODO:
Implemented conversation memory by following: https://python.langchain.com/v0.2/docs/how_to/message_history/
This implementation is not using conversation summary buffer memory
Right now, it can't answer the question: "List out all of my previous questions", to which it responds "I don't know".
I need to figure out how to debug what is being sent to ChatGPT 3.5
I need to figure out how to implement a conversation summary buffer memory to optimize
"""

import os
from typing import List
import psycopg
from langchain_openai import ChatOpenAI
from langchain_postgres import PostgresChatMessageHistory
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.memory.summary_buffer import ConversationSummaryBufferMemory

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
        
    def get_session_history(self, session_id) -> BaseChatMessageHistory:
        pg_chat_message_history = PostgresChatMessageHistory(
            self.table_name,
            session_id,
            sync_connection=self.sync_connection
        )
        
        conversation_buffer_memory = ConversationSummaryBufferMemory(
            llm=self.chat_model,
            chat_memory = pg_chat_message_history,
            memory_key='history'
        )

        # TODO: FIGURE OUT WHAT TO RETURN, CHANGE THIS OR THE CHAIN
        return conversation_buffer_memory.chat_memory
        
    def get_inference_with_context(self, session_id: str, query: str, context: List[Document]):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    SYSTEM: You are a helpful AI Assistant.
                    
                    Answer the question by only responding with the information from the CONTEXT or chat history. Otherwise say you don't know.
                    
                    Your response also must include the all sources of your answer.
                        - Video transcript sources need time stamps
                        - Chat history sources need a quote and distinguishes user or ai.
                    
                    CONTEXT:
                    {context}
                    """,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{query}"),
            ]
        )
        
        runnable = prompt | self.chat_model 
        
        runnable_with_history = RunnableWithMessageHistory(
            runnable,
            self.get_session_history,
            input_messages_key="query",
            history_messages_key="history",
        )
        
        # Format the context for the prompt
        context_content = " ".join([doc.page_content for doc in context])

        response = runnable_with_history.invoke(
            {"context": context_content, "query": query},
            config={"configurable": {"session_id": session_id}},
        )

        # Use the chain with memory
        return response
        