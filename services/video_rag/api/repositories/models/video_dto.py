from datetime import datetime
from sqlalchemy import Boolean, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from services.video_rag.api.repositories.models import Base
from services.video_rag.api.repositories.models.session_dto import SessionDto # NOTE: This reference would break microservice architecture. In the future, create a VideoSession class so that a seperate video service would have all the info it needs, and would grab what it needs from a Session Service

class VideoDto(Base):
    __tablename__ = 'video'
    
    video_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_video_id: Mapped[str] = mapped_column(String, nullable=False)
    session_id: Mapped[str] = mapped_column(ForeignKey(SessionDto.get_primary_key_with_table(), ondelete="CASCADE"))
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Relationships
    # TODO: Progamatically get VideoDto name from class
    session = relationship("SessionDto", back_populates="videos")
