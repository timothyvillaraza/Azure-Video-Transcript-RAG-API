# Include Base Metadatas 

from services.video_rag.api.repositories.models import Base as video_rag_base

autogenerate_base_metadatas = [
    video_rag_base.metadata,
    # Other service models
]