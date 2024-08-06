from services.video_rag.api.repositories.models import Base
from services.common.repositories.mixins.primary_key_mixin import PrimaryKeyMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String, DateTime 
from datetime import datetime

class SessionDto(Base, PrimaryKeyMixin):
    __tablename__ = 'session'
    
    session_id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
