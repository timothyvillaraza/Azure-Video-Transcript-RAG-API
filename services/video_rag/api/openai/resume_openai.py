import os
from openai import OpenAI
from typing import List
from langchain.docstore.document import Document
from services.video_rag.api.services.models.resume_inference_model import ResumeInferenceModel

class ResumeOpenAI: 
    async def get_resume_inference_async(self, query, documents: List[Document]):
        client = OpenAI(api_key=os.getenv('OPENAI_KEY'))
        
        context = "Below is a list of context sources. What ever is mentioned MUST be included in context sources to trace back the source of the info:"
        for doc in documents:
            context += f"{doc.page_content}\n"
        
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are an interactive chat interface answering questions regarding the resume of Timothy Villaraza. Provide both the llm response and context sources that were used in the response. The response must brief at 50 - 80 words max."},
                {"role": "system", "content": context},
                {"role": "user", "content": query},
            ],
            response_format=ResumeInferenceModel
        )
        
        return completion.choices[0].message.parsed