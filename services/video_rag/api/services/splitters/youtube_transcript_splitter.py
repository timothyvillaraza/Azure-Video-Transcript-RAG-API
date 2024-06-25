from typing import List
from langchain.text_splitter import TextSplitter

class YouTubeTranscriptSplitter(TextSplitter):
    def __init__(self, captions_per_chunk=1000):
        self.captions_per_chunk = captions_per_chunk

    def split(self, transcripts: List[str]) -> List[str]:
        chunks = []
        current_chunk = ''
        captions_per_overlap = 5
        
        for video_id, captions in transcripts.items():
            # Write each caption to the file
            for j in range(len(captions)):
                caption = captions[j]
                current_chunk += f"{caption['start']}: {caption['text']}\n"
                
                # Prepare next chunk if the size is met
                if j != 0 and j % self.captions_per_chunk == 0:
                    chunks.append(current_chunk)
                    
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
            
        return chunks