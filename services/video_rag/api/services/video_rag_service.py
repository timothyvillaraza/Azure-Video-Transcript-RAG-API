import os
import langchain
from typing import Dict, List
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings


from services.video_rag.api.services.models.save_video_transcript_model import TranscriptEmbeddingsModel
from services.video_rag.api.services.youtube_transcript_service import YouTubeTranscriptService
from services.video_rag.api.repositories.transcript_repository import TranscriptRepository

class VideoRagService:
    def __init__(self):
        self._youtubeTranscriptService = YouTubeTranscriptService()
        self._transcriptRepository = TranscriptRepository()
    
    def save_video_transcript_embeddings(self, video_ids: List[str]) -> TranscriptEmbeddingsModel:
        # Get Transcripts
        transcripts, failed_video_ids = self._youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        # Create Langchain Documents from chunked transcripts
        transcript_chunks_documents = _create_documents(transcripts)
        
        # Save documents
        transcript_embeddings_dto = self._transcriptRepository.save_transcript_embeddings(transcript_chunks_documents)
        
        # Collect failed video ids from the transcript api and the embedding process for returning it to the function
        failed_video_ids.extend(transcript_embeddings_dto.failed_video_ids)
        
        # Map from repository dto to service model
        transcript_embeddings_model =  TranscriptEmbeddingsModel(transcript_embeddings_dto.successful_video_ids, failed_video_ids)
        
        return transcript_embeddings_model
    
    def get_video_transcript(self, video_ids: List[str]):
        tempModelResponse = TranscriptEmbeddingsModel()

        self._youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        # Chunk Transcripts
        # Embed Transcripts
        # Save Transcripts to PG Vector
        
        return tempModelResponse

# Helper Function
def _create_documents(transcripts: Dict[str, List[Dict[str, str]]]) -> Dict[str, List[Document]]:
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