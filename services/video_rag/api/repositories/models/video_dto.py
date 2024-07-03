from services.video_rag.api.repositories.models import Base 
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import List

class VideoDto(Base):
    __tablename__ = 'video'
    
    video_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    create_date: Mapped[datetime]
    test_id: Mapped[int]
    