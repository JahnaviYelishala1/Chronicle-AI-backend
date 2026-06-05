from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db.database import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)

    video_id = Column(
        Integer,
        ForeignKey("videos.id"),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )