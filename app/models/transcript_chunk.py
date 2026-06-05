from sqlalchemy import Column, Integer, Text, ForeignKey

from app.db.database import Base


class TranscriptChunk(Base):
    __tablename__ = "transcript_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    transcript_id = Column(
        Integer,
        ForeignKey("transcripts.id"),
        nullable=False
    )

    chunk_text = Column(
        Text,
        nullable=False
    )