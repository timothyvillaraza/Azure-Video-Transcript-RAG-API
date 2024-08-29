import logging
import requests
from bs4 import BeautifulSoup, Comment

from typing import Dict, List
from datetime import datetime
from langchain.docstore.document import Document
# Services
from services.video_rag.api.services.youtube_transcript_service import YouTubeTranscriptService
# Repositories
from services.video_rag.api.repositories.transcript_repository import TranscriptRepository
# Chains
from services.video_rag.api.langchain.video_rag_chain import VideoRAGChain
from services.video_rag.api.openai.resume_openai import ResumeOpenAI
# Models
from services.video_rag.api.services.models.inference_model import InferenceModel
from services.video_rag.api.services.models.resume_inference_model import ResumeInferenceModel
from services.video_rag.api.services.models.transcript_embedding_model import TranscriptEmbeddingsModel

class VideoRagService:
    def __init__(self):
        self._youtubeTranscriptService = YouTubeTranscriptService()
        self._transcriptRepository = TranscriptRepository()
    
    def save_video_transcript_embeddings(self, session_id: str, video_ids: List[str]) -> TranscriptEmbeddingsModel:
        # Get Transcripts
        transcripts, failed_video_ids = self._youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        if failed_video_ids:
            logging.error(f'YouTubeTranscript API Error: Could not retrieve transcripts for {failed_video_ids}')
        
        # Create Langchain Documents from chunked transcripts
        transcript_chunks_documents = _create_transcript_documents(transcripts)
        
        # Save documents
        transcript_embeddings_dto = self._transcriptRepository.save_transcript_embeddings(session_id, transcript_chunks_documents)
        
        # Collect failed video ids from the transcript api and the embedding process for returning it to the function
        failed_video_ids.extend(transcript_embeddings_dto.failed_video_ids)
        
        # Map from repository dto to service model
        transcript_embeddings_model =  TranscriptEmbeddingsModel(transcript_embeddings_dto.successful_video_ids, failed_video_ids)
        
        return transcript_embeddings_model
    
    async def get_inference_async(self, session_id: str, query: str, create_date: datetime) -> InferenceModel:
        # Get Relevant Documents from Repository
        retrieved_documents_score_tuples = await self._transcriptRepository.get_by_semantic_relevance_async(session_id=session_id, query=query, results_count=1)
        
        # TODO: Optimize Retrevial by cleaning up embedded document sources (currently each chunk contains timestamps), adding additional heuristics, or changing the embedding model
        # TODO: Example: [document for doc, score in docs_with_score if score > 0.8]
        retrieved_documents = [document for document, score in retrieved_documents_score_tuples]
        
        # Save user message, get LLM response, save LLM response 
        video_rag_chain = VideoRAGChain()
        llm_response = video_rag_chain.get_inference_with_document_context(session_id, query, retrieved_documents)
        
        inference_model = InferenceModel(response=llm_response)
        
        return inference_model
    
    async def get_resume_inference_async(self, query: str) -> ResumeInferenceModel:
        # Get Relevant Documents from Repository
        retrieved_documents_score_tuples = await self._transcriptRepository.get_by_semantic_relevance_async(session_id='resume', query=query, results_count=20)
        
        # TODO: Optimize Retrevial by cleaning up embedded document sources (currently each chunk contains timestamps), adding additional heuristics, or changing the embedding model
        # TODO: Example: [document for doc, score in docs_with_score if score > 0.8]
        retrieved_documents = [document for document, score in retrieved_documents_score_tuples]
        
        # Save user message, get LLM response, save LLM response 
        resume_openai = ResumeOpenAI()
        llm_response = await resume_openai.get_resume_inference_async(query, retrieved_documents)
        
        return llm_response
    
    async def save_resume_embeddings_from_iframe(self, url: str) -> None:
        iframe_content = requests.get(url)
        
        if iframe_content.status_code == 200:
            iframe_html_content = iframe_content.text

            soup = BeautifulSoup(iframe_html_content, 'lxml')

            resume_texts = _extract_all_text(soup)
            
            documents = [Document(page_content=text) for text in resume_texts]
            
            await self._transcriptRepository.save_resume_embeddings(documents)
        else:
            print(f"Failed to retrieve content from {url}")
        
        return
      
    async def delete_resume_embeddings(self) -> None:
        await self._transcriptRepository.delete_resume_embeddings()
        return
        

# =======================================
# Helper Functions
# =======================================
def _create_transcript_documents(transcripts: Dict[str, List[Dict[str, str]]]) -> Dict[str, List[Document]]:
    # Return
    created_documents = {}
    
    # Convert Video Transcript into Chunks
    chunks = []
    current_chunk = ''
    captions_per_chunk = 50
    captions_per_overlap = 5
    
    for video_id, captions in transcripts.items():
        documents = []
        
        for j in range(len(captions)):
            caption = captions[j]
            current_chunk += f"{caption['start']}: {caption['text']}\n"
            
            # Prepare next chunk if the size is met
            if j != 0 and j % captions_per_chunk == 0:
                chunks.append(current_chunk)
                documents.append(
                    Document(
                        page_content=current_chunk,
                        metadata={"video_id": video_id, "video_name": "TODO: GET TITLE"} # TODO: Get Video Title
                    )
                )
                
                #
                # Setup next chunk for overlap
                #
                current_chunk = ''
                
                # Overlap Chunks
                if j >= captions_per_overlap:
                    for previous_chunk_caption in captions[j - (captions_per_overlap - 1): j]:
                        current_chunk += f"{previous_chunk_caption['start']}: {previous_chunk_caption['text']}\n"
        
        # Capture last of captions 
        chunks.append(current_chunk)
        documents.append(
            Document(
                page_content=current_chunk,
                metadata={"video_id": video_id, "video_name": "TODO: GET TITLE"} # TODO: Get Video Title
            )
        )
        
        created_documents[video_id] = documents
        
    return created_documents    

def _extract_all_text(soup) -> set[str]:
    all_text_elements = set()

    for element in soup.find_all(text=True):
        # Exclude text from script, style, and similar non-visible elements
        if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            # Exclude comments and non-visible elements
            if not isinstance(element, Comment):
                text = element.strip()  # Remove leading/trailing whitespace
                if text and not element.isspace() and len(text) > 1:  # Only add non-empty strings and skip whitespace
                    all_text_elements.add(text)

    return all_text_elements