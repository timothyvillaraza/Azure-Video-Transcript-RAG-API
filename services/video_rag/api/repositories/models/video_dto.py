from services.video_rag.api.repositories.models import Base 
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
from datetime import datetime

class VideoDto(Base):
    __tablename__ = 'video'
    
    video_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_video_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    session_id: Mapped[str] = mapped_column(String, nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
