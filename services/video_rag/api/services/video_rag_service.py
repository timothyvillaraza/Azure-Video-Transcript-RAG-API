import os
import langchain
from typing import Dict, List
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings


from services.video_rag.api.services.models.save_video_transcript_model import SaveVideoTranscriptmodel
from services.video_rag.api.services.youtube_transcript_service import YouTubeTranscriptService
from services.video_rag.api.repositories.transcript_repository import TranscriptRepository

class VideoRagService:
    def __init__(self):
        self._youtubeTranscriptService = YouTubeTranscriptService()
        self._transcriptRepository = TranscriptRepository()
    
    def save_video_transcript(self, video_ids: List[str]):
        tempModelResponse = SaveVideoTranscriptmodel()

        # Get Transcripts
        transcripts = self._youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        # Create Langchain Documents from chunked transcripts
        transcript_chunks_documents = _create_documents(transcripts)
        
        # Save document
        tempModelResponse = self._transcriptRepository.save_transcript_embeddings(transcript_chunks_documents)
        
        return tempModelResponse
    
    def get_video_transcript(self, video_ids: List[str]):
        tempModelResponse = SaveVideoTranscriptmodel()

        self._youtubeTranscriptService.get_youtube_transcripts_async(video_ids)
        
        # Chunk Transcripts
        # Embed Transcripts
        # Save Transcripts to PG Vector
        
        return tempModelResponse

def _create_documents(self, transcripts: Dict[str, List[Dict[str, str]]]) -> List[str]:
    # Collection of Document class objects created for each chunk
    documents = []
    
    # Convert Video Transcript into Chunks
    chunks = []
    current_chunk = ''
    captions_per_chunk = 50
    captions_per_overlap = 5
    
    for video_id, captions in transcripts.items():
        # Write each caption to the file
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
                # Next Chunk Setup
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
        
    return documents